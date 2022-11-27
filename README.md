# About The Project

This project is focused on deploying on Google cloud.

## Installation

1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

### Development

1. Create .env (`cp .env.template .env`) file with related environment variables
2. `python manage.py runserver` or `bash docker-entrypoint.sh`
3. To run with Google cloud DB see [this](https://cloud.google.com/python/django/appengine#run-locally)

<p align="right">(<a href="#top">back to top</a>)</p>

### Google cloud

1. See [this](https://cloud.google.com/python/django/appengine)

<p align="right">(<a href="#top">back to top</a>)</p>

## Testing

For unit tests:
1. `export TRAMPOLINE_CI='1'`
2. `python manage.py test`
