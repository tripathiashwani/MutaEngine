# MutaEngine Career Backend

## setup

```sh
git clone https://github.com/MutaEngine/backend_career_website.git
cd backend_career_website
```

Create a virtual environment

```sh
python -m venv venv
```

using window

```sh
venv/Scripts/activate
```

using unix based system

```sh
source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

migrate the database

```sh
python manage.py migrate
```

run Django project

```sh
python manage.py runserver
```