# Getting wagtail prototype up and running on your computer

1. install pipenv (if you havent already)
```bash
pip install pipenv
```
2. run pipenv install to get all the dependancies for the project and install them in a virtual enviroment
```bash
pipenv install 
```
3. activate the virtual environment (check the virtual env is visible in your terminal after this command)
```bash
pipenv shell 
```
4. run wagtail
```bash
wagtail manage.py runserver
```