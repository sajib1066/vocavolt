# Vocavolt
Charge Up Your Vocabulary

[![python-version](https://img.shields.io/badge/Python-3.11.6-blue)](https://www.python.org/)
[![django-version](https://img.shields.io/badge/Django-4.2.7-green)](https://www.djangoproject.com/)


## Development Setup

1. Create a repository using this template or clone the repository
   ```
   git clone git@github.com:sajib1066/vocavolt.git
   ```
2. Create a virtual environment
   ```
   python -m venv venv
   ```
3. Activate the virtual environment
   ```
   source venv/bin/activate
   ```
4. Install modules
   ```
   pip install -r requirements.txt
   ```
5. Create local settings
   ```
   cp examples/local_settings.example vocavolt/local_settins.py
   ```
6. Create logs file
   ```
   mkdir logs
   ```
7. Migrate database
   ```
   python manage.py migrate
   ```
8. Create superuser
    ```
    python manage.py createsuperuser
    ```
9. Run the project
    ```
    python manage.py runserver
    ```
