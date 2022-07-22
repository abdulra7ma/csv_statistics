# CSV Statistics

## Table of contents
- [CSV Statistics](#csv-statistics)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [APP-LOGIC](#app-logic)
    - [what i should do?](#what-i-should-do)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)

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

## APP-LOGIC
Normally when initiating a copy of this project and run it, there is not garente that any statitistical calculation gonna happen until you upload a copy of the csv file that contains statitistical data.

### what i should do?
1. upload a valid csv file to the upload-csv endpoint
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/self-service/statistics/upload-csv' \
--header 'Cookie: csrftoken=t9SuMsIvbz18aoYLfM6ZMt7PTJ9wBEKH3XRIERRGv21Acz4gkHoZ8P9eqkOsyChj' \
--form 'file=@"machine-full-path/test_data.csv"'
```

2. if the given csv file was valid than a triggered event on the server gonna generate statitistical calculation and save the output to the database. Then you gonna have the ability to request the calculated data and perform filters over it.
   1. request example:
      ```
      curl -X 'GET' \
      'http://127.0.0.1:8000/api/v1/statistics/?type=Lower%20A&info_count=1252&errors_count=1252' \
      -H 'accept: application/json' \
      -H 'X-CSRFToken: NyBYCU01QcQVsBn6M853zM5xhDBItC1LLApIP03pvW4U4xq8fDlzTDvm9mgxoFg8'
      ```
    2. response sample:
        ```
        {
          "count": 1,
          "next": null,
          "previous": null,
          "results": [
            {
              "aircraft": null,
              "status": null,
              "type": "Lower A",
              "info_count": 1252,
              "errors_count": 1252,
              "pre_legend": 0,
              "warning": 0,
              "paired_b": 0,
              "legend": 0,
              "lower_b": 0,
              "repeat_legend": 0,
              "upper_a": 0,
              "lower_a": 1252,
              "paired_a": 0
            }
          ]
        }
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
