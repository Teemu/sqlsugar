# SQLSugar - Automatic migrations for SQLAlchemy

[![PyPI](https://img.shields.io/pypi/v/sqlsugar.svg)](https://pypi.org/project/sqlsugar/)
[![Changelog](https://img.shields.io/github/v/release/Teemu/sqlsugar?include_prereleases&label=changelog)](https://github.com/Teemu/sqlsugar/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Teemu/sqlsugar/blob/main/LICENSE)

This library is for you if you want to use a real database without spending time to generate migrations. This is experimental and you should switch to [Alembic](https://alembic.sqlalchemy.org/en/latest/) as your project matures. This only supports adding new tables, columns and indexes.

## Installation

Install this library using `pip`:

    pip install sqlsugar

## Usage

Look for examples with [SQLAlchemy](https://github.com/Teemu/sqlsugar/blob/main/examples/use_with_sqlalchemy.py) or [SQLModel](https://github.com/Teemu/sqlsugar/blob/main/examples/use_with_sqlmodel.py).

```python
from sqlsugar import migrate

migrate(engine.connect(), Base.metadata)
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd sqlsugar
    python -m venv .venv
    source .venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'
    pre-commit install

To run the tests:

    pytest
