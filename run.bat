python -m venv .venv
cd .venv\Scripts
call activate.bat
cd ..\..
pip install -r requirements.txt
cd project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
