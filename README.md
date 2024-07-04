# AVIATO RBAC

Role Based Access Control Endpoints

## Basic requirements to run this code

- Python3.11.9
- PostgreSQL 15

## Install dependencies

Install `pipenv` dependency management

```
pip3 install pipenv
```

Pipenv useful commands

```
# Use created virtual env
pipenv --python 3.11

# Install all dependencies:
pipenv install --dev

# Use created virtualenv
pipenv shell
```

## Steps to setup Database locally

- Create database in the PostgreSQL
- Create a schema under the database
- Update the env file with the database configuration
- Run `alembic upgrade head` to create the latest database schema

## Steps to start the server locally

- Update the env file with required details
- Run `sh start_server.sh` to start the server
