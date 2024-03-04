# digi-khedmat
backend and frontend services source code for digi-khedmat web application. (digi-khedmat.ir)


## Prerequisites
- Python -> full experience in python projects
- Django -> experience in main concepts of django
- DRF -> experience in restfull api apps
- Javascript -> experience in ES4 to ES7
- Understanding of HTML and CSS
- TailwindCss -> experience in tailwindcss styling frontend apps

## Required Software
- [Python 3.10](https://www.python.org/downloads/) or newer
- [Node.js 18.15 LTS](https://nodejs.org/) or newer (For Tailwind.CSS)
- [Git](https://git-scm.com/)


### Required python package Manager
we need a Python packaging and dependency management, so we use [poetry](https://python-poetry.org/).

## Getting Started
```bash
mkdir -p digi_khedmat
cd digi_khedmat
git clone https://github.com/sinasezza/digi-khedmat.git
cd digi-khedmat
```


### Configure Environment
_macOS/Linux Users_
```bash
python manage.py -m venv venv
source ./venv/bin/activate
pip install poetry
poetry install
```

_Windows Users_
```bash
python manage.py -m venv venv
venv\scripts\activate
pip install poetry
poetry install
```


### Configure and Run TailwindCss
```bash
poetry run python mange.py tailwind install
poetry run python manage.py tailwind start
```

### Configure Node Packages
```bash
poetry run python manage.py node_packages install
```

### Run The Django Http Server
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```

