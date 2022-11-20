import logging

from alembic.operations import Operations
from alembic.operations.ops import (
    AddColumnOp,
    CreateIndexOp,
    CreateTableOp,
    ModifyTableOps,
)

logger = logging.getLogger(__name__)


class DiffToOperation:
    def __init__(self, operations: Operations) -> None:
        self.op = operations

    def CreateTableOp(self, op: CreateTableOp) -> None:
        logger.info("%s Creating a table: %r", op.table_name, op)
        op.to_table().create(bind=self.op.migration_context.connection)

    def AddColumnOp(self, op: AddColumnOp) -> None:
        logger.info("%s: Adding a column to %r", op.table_name, op)
        self.op.add_column(op.table_name, op.column)  # type: ignore

    def ModifyTableOps(self, op: ModifyTableOps) -> None:
        logger.info("%s: Modifying a table", op.table_name)
        for op2 in op.ops:
            name = op2.__class__.__name__
            if hasattr(self, name):
                getattr(self, name)(op2)
            else:
                table_name = getattr(op2, "table_name", "")
                logger.warn(
                    "%s: Unsupported operation for %r",
                    table_name,
                    op2.__class__.__name__,
                )

    def CreateIndexOp(self, op: CreateIndexOp) -> None:
        logger.info("Creating an index: %s %r", op.table_name, op)
        self.op.create_index(  # type: ignore
            op.index_name, op.table_name, [x.name for x in op.to_index().expressions]
        )
