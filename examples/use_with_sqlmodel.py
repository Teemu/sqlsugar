import logging
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

from sqlsugar import migrate

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Try uncommenting this to create a new column:
    # age: Optional[int] = Field(default=10)

    # Try uncommenting this to create a new column with an index:
    # age: Optional[int] = Field(default=10, index=True)


engine = create_engine("sqlite:///example.db")

migrate(engine.connect(), SQLModel.metadata)


with Session(engine) as session:
    cat = Cat(name="Meow")
    session.add(cat)
    session.commit()

    print("%i cats" % session.query(Cat).count())
