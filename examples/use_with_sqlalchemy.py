import logging

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from sqlsugar import migrate

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


Base = declarative_base()


class Cat(Base):
    __tablename__ = "cat"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Try uncommenting this to create a new column:
    # age = Column(Integer, nullable=True, default=10)

    # Try uncommenting this to create a new column with an index:
    # age = Column(Integer, nullable=True, default=10, index=True)


engine = create_engine("sqlite:///example.db")

migrate(engine.connect(), Base.metadata)


with Session(engine) as session:
    cat = Cat(name="Meow")
    session.add(cat)
    session.commit()

    print("%i cats" % session.query(Cat).count())
