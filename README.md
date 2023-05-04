![ci](https://github.com/Fiufit-Grupo-10/python-template/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Fiufit-Grupo-10/python-template/branch/main/graph/badge.svg?token=0QRZ6NO0R1)](https://codecov.io/gh/Fiufit-Grupo-10/python-template)

# FiuFit-Trainers

Microservice users implementation for Fiufit application

## Running dev enviroment:

To set up the development environment for this microservice, you need to have Docker and Docker Compose installed on your machine.
### 1. Clone this repository

```bash
git clone git@github.com:Fiufit-Grupo-10/FiuFit-Users.git
```
### 2. Navigate to the cloned repository and execute

```bash
sudo docker-compose -f docker-compose-testing.yml up --build
```

### 3. Run this command in a new terminal to complete the initialization of the database service

```bash
sudo docker-compose -f docker-compose-testing.yml exec db psql --username=fiufit --dbname=fiufit_users_dev -f /docker-entrypoint-initdb.d/insert_tt.sql    
```

## To run tests or other commands on the container:

```bash
sudo docker-compose -f docker-compose-testing.yml exec <command>
```
### Examples

To access the PostgreSQL service through the command line

```bash
sudo docker-compose -f docker-compose-testing.yml exec db psql --username=fiufit --dbname=fiufit_users_dev
```
To run tests

```bash
docker-compose -f docker-compose-testing.yml exec web pytest -v
```
