import logging
from enum import Enum, auto

from alembic.autogenerate import produce_migrations
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import MetaData
from sqlalchemy.engine import Connection

from .exceptions import UnsupportedOperation
from .operations import DiffToOperation

logger = logging.getLogger(__name__)


class MigrationErrorType(Enum):
    IGNORE = auto()
    WARN = auto()
    ERROR = auto()


def migrate(
    connection: Connection,
    metadata: MetaData,
    error_unused: MigrationErrorType = MigrationErrorType.WARN,
) -> None:
    assert isinstance(error_unused, MigrationErrorType)

    mc = MigrationContext.configure(connection)
    migrations = produce_migrations(mc, metadata)
    upgrade_ops = migrations.upgrade_ops.ops

    context = MigrationContext.configure(connection)
    operations = Operations(context)
    diff_to_operation = DiffToOperation(operations)

    operation_names = []

    for op in upgrade_ops:
        name = op.__class__.__name__
        operation_names.append(name)
        if name == "ModifyTableOps":
            for op2 in op.ops:
                operation_names.append(op2.__class__.__name__)

    for name in operation_names:
        if not hasattr(diff_to_operation, name):
            if error_unused is MigrationErrorType.IGNORE:
                pass
            elif error_unused is MigrationErrorType.WARN:
                logger.warn("Unsupported operation %s", name)
            elif error_unused is MigrationErrorType.ERROR:
                raise UnsupportedOperation(name)

    for op in upgrade_ops:
        name = op.__class__.__name__
        if hasattr(diff_to_operation, name):
            getattr(diff_to_operation, name)(op)

    unsupported_upgrade_ops = [
        name for name in operation_names if not hasattr(diff_to_operation, name)
    ]

    if unsupported_upgrade_ops:
        logger.warn(
            "%i operations, %i unsupported",
            len(upgrade_ops),
            len(unsupported_upgrade_ops),
        )
    else:
        logger.info("%i operations", len(upgrade_ops))

    return None
