# Companies API


## Local Installation

Inside CompaniesAPI dir run the following commands:

### - Postgres
It's recommended to use Postgres with Docker. To do it Run:


`docker run -d -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres --name posttest -p 5432:5432 postgres`

To create the database run:
`psql -h 127.0.0.1 -p 5432 -U postgres`

The password is "postgres"

After connecting to Postgres run:

`create database companies_api with owner postgres;`

The local database will be created.

### - Create a virtual ENV
`python3 -m venv .venv`

### - Activate the virtual ENV
`source ./.venv/bin/activate`

### - Install requirements
`pip install wheel`

`pip install -r requirements.txt`

### - Run the migrations
`python manage.py migrate`

## Running the tests
To run the tests use:
`python manage.py test`

## Running the server
To run the server use:
`python manage.py runserver`

## For running with Docker
Inside CompaniesAPI dir:
`docker-compose up`

## API Docs
To see the API docs you first need to create a superuser and login to django admin:
`python manage.py createsuperuser`

Login to django admin in http://127.0.0.1:8000/admin/

And with your server running navigate to http://127.0.0.1:8000/docs/

