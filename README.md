Python Django Back-end for Task Manager App-------------------------


Installation 
--------------------------------------------------------------
-Install Python latest stable version

-Install Packages that is given in requirements.txt


if you want to install packages on a virtual environment then you can follow the steps below----------------------

- create a new folder for project and enter the folder
- Extract the project folder here
- open created new folder on CMD(Command prompt)

create venv --------------------

- python -m venv venv

activate venv ---------------------

- venv\Scripts\activate

Install Packages---------------------

- go inside of the project folder (Task_Manager(python))
- pip install -r requirements.txt

if you want to install packages globally then you can follow the steps below----------------------

- create a new folder for project and enter the folder
- Extract the project folder here
- open created new folder on CMD(Command prompt)

- go inside of the project folder (Task_Manager(python))
- pip install -r requirements.txt

-----------------------------------------------------------------------

Run

------------------------------------------------------------------------
before running you have to create migration files and migrate it

- python manage.py makemigrations
- python manage.py migrate

after this your database will be created

If you Want to create superuser then run this command and give user credentials

- python manage.py createsuperuser


now you can run the project

- python manage.py runserver

this command will run the project on the default local host (http://127.0.0.1:8000).
make sure the local host address is same given example.

If you want to login to Admin page you can go to the url - http://127.0.0.1:8000/admin/
and give superuser credentials.


now you can go to react app

