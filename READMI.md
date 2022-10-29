# Project name
CX DOJO test

# General info
test app for CX DOJO

# Technologies
* python 3
* django 4.1
* PostgreSQL

# Setup

Clone the project Repository
```
$ git clone https://github.com/SergiiPachkovskyi/Avto_net
```

Enter the project folder and create a virtual environment
``` 
$ cd django_project

$ python -m venv venv 
```

Activate the virtual environment
``` 
$ . venv/bin/activate # On Linux or Unix

$ . venv/Scripts/activate # On Windows  
```

Install requirements

```
$ pip install -r requirements.txt
```

Install psycopg2

```
$ pip install psycopg2-binary # On Linux or Unix
$ pip install psycopg2 # On Windows
```

Refill django_project/django_project/.env


Create database

``` 
$ python django_project/create_db.py
```

Make migrations and create a superuser
``` 
$ python manage.py migrate
$ python manage.py createsuperuser
``` 

Run the project in development 
``` 
$ python manage.py runserver
```

# Status
Project is: in progress