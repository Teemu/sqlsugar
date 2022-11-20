from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from sqlsugar import MigrationErrorType, migrate


def test_creating_database():
    Base = declarative_base()

    class Dog(Base):
        __tablename__ = "dog"

        id = Column(Integer, primary_key=True)
        name = Column(String)

    engine = create_engine("sqlite:///:memory:")

    migrate(engine.connect(), Base.metadata, error_unused=MigrationErrorType.ERROR)

    with Session(engine) as session:
        dog = Dog(name="Bark")
        session.add(dog)
        session.commit()

        assert session.query(Dog).count() == 1


def test_adding_a_column():
    Base = declarative_base()

    class Dog(Base):
        __tablename__ = "dog"

        id = Column(Integer, primary_key=True)
        name = Column(String)

    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    migrate(connection, Base.metadata, error_unused=MigrationErrorType.ERROR)
    context = MigrationContext.configure(connection)
    operations = Operations(context)
    operations.drop_column("dog", "name")
    migrate(connection, Base.metadata, error_unused=MigrationErrorType.ERROR)

    with Session(engine) as session:
        dog = Dog(name="Bark")
        session.add(dog)
        session.commit()

        assert session.query(Dog).count() == 1


def test_adding_a_index():
    Base = declarative_base()

    class Dog(Base):
        __tablename__ = "dog"

        id = Column(Integer, primary_key=True)
        name = Column(String, index=True)

    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    migrate(connection, Base.metadata, error_unused=MigrationErrorType.ERROR)
    context = MigrationContext.configure(connection)
    operations = Operations(context)
    operations.drop_index("ix_dog_name", "dog")
    migrate(connection, Base.metadata, error_unused=MigrationErrorType.ERROR)

    with Session(engine) as session:
        dog = Dog(name="Bark")
        session.add(dog)
        session.commit()

        assert session.query(Dog).count() == 1
