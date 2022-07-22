# CSV Statistics

## Table of contents
- [CSV Statistics](#csv-statistics)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)
  - [Notes](#notes)

## Setup
1. install pipenv 
```
pip install pipenv

```
2. install needed packages and activate the venv
```
pipenv install
pipenv shell
```

## run in dev environment

1. migrate database
```
fab django.migrate
```
2. run development server
```
fab run
```


## Run it with docker
1. docker compose up
```
fab compose.up
```
