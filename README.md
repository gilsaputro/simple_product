# Simple-Product-Apps
This repository contains the prototype for an Simple Product Application.

## Getting Started
These intruction will get you a project and how to run the binary on your local machine.

### Prerequsites
The Simple Product management system requires Python 3.11.2 or higher and Docker installed on the local machine in order to run the binary.

#### Docker
You need to have docker installed in your machine.
Follow this step if you don't have docker on your machine :
- Download the Docker CE (Community Edition) package from the Docker website (https://www.docker.com/products/docker-desktop).
- Install the package by following the instructions provided during the installation process.
- Once the installation is complete, verify that Docker has been installed correctly by running the following command in your terminal: "docker run hello-world".

#### Python Programming Language
You need to have Python 3.11.2 installed in your machine.
Follow this step if you don't have Python on your machine :
- Download the Python binary package from the official Python website (https://www.python.org/downloads/).
- Install the package by following the instructions provided during the installation process.
- Once the installation is complete, verify that Python has been installed correctly by running the following command in your terminal: "python --version".

## How to run locally

### TLDR
```
# clone project
git clone https://github.com/gilsaputro/simple_product.git
cd simple_product

# installing dependency
pip install -r requirements.txt

# init docker
make deps-init

# migrate table (create table)
make migrate-up

# run binary
make run-local
```

### Clone Repository:
Once you have all the prerequisites properly installed, you can start by cloning this repository.
- To clone the repository, run the following command in your terminal:
```
git clone https://github.com/gilsaputro/simple_product.git
```
- To navigate to the repository directory, run the following command in your terminal:
```
cd simple_product
```
Note: These instructions assume that you have Git installed on your machine. If you don't have Git installed, you can follow the instructions on the Git website to install it.

### Setup Project Dependency:
Once you are in the project directory, you must first install the required dependencies from the requirements.txt file. You can do this by running the following command:

```
pip install -r requirements.txt
```

### Docker Setup:
To run the Simple Product management system binary correctly, it is necessary to connect it with the related dependencies. This can be done simply by executing the following command: 

```azure
make deps-init
```

The deps-init command will perform the following actions:
- Build Vault and store secrets
- Build Redis and verify that it is running
- Build Postgres and verify that it is running

To stop the dependencies, run :
```azure
make deps-tear
```

### Migrate Table
Once you have the project dependencies installed and running, it's time to set up the database tables and dependencies. To do this, execute the following command:

```azure
make migrate-up
```

This command will perform the following actions:
- Apply database migrations: It will use Alembic to create or update the necessary tables and dependencies in your database, ensuring it's ready for use.


To revert the applied migrations, you can execute:
```azure
make migrate-down
```
This command will:
- Rollback database changes: It will use Alembic to revert the database to a previous state, undoing the most recent migration.


### Running Binary:
Once you have cloned the repository and set up all the dependencies, you can run the binary using either of the following methods:

Note: If you have change the docker config please change the config in /config/config.yaml before run it

And run using :

```
python app.py
```

or 

```
make run-local
```


### Postman Collection
You can import postman collection in Repo File with Name : 
```
Aquafarm Management System.postman_collection.json
```

Note: The details mentioned in these steps may vary depending on your configuration.