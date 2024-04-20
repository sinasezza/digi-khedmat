# digi-khedmat

Welcome to digi-khedmat! This repository contains the source code for both the backend and frontend services of the digi-khedmat web application ([digi-khedmat.ir](https://digi-khedmat.ir)).

## Overview

digi-khedmat is a web application aimed at providing various services to users, including but not limited to, digital services, exchanges, and advertisements. The project is built using Django for the backend, Django Rest Framework (DRF) for building RESTful APIs, and modern JavaScript with Tailwind CSS for the frontend.

## Features

- **Digital Services:** Users can avail various digital services offered through the platform.
- **Exchanges:** Facilitates the exchange of goods and services among users.
- **Advertisements:** Allows users to create and manage advertisements for their products or services.

## Prerequisites

To work with this project, you'll need:

- **Python:** Full experience in Python projects, preferably Python 3.10 or newer.
- **Django:** Experience in the main concepts of Django.
- **Django Rest Framework (DRF):** Experience in building RESTful API apps.
- **JavaScript:** Proficiency in ES4 to ES7.
- **HTML and CSS:** Understanding of basic HTML and CSS.
- **Tailwind CSS:** Experience in using Tailwind CSS for styling frontend apps.

## Required Software

Ensure you have the following software installed:

- [Python 3.10](https://www.python.org/downloads/) or newer
- [Node.js 18.15 LTS](https://nodejs.org/) or newer (required for Tailwind CSS)
- [Git](https://git-scm.com/)

## get the repository
```bash
git clone https://github.com/sinasezza/digi-khedmat.git
cd digi-khedmat
```

## Setup


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

### Configure Environment Variables
Create `.env` file on the root directory and use following content:
- dotenv is used to hide sensitive information like database password from public access.
- you can use .samples (.env.dev or .env.prod) as template for your own environment variables.
- just rename the .sample file to '.env' and use it.


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

