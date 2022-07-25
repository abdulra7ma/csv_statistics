# CSV Statistics

## Table of contents
- [CSV Statistics](#csv-statistics)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [APP-LOGIC](#app-logic)
    - [what i should do?](#what-i-should-do)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)
  - [run test files](#run-test-files)

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
> **_NOTE:_** uploading the same file won't load any data to the database as every file has a generated hash after being uploaded to server. so if you want to load the same data to the database you got to change let bit in the file internels. 

1. if the given csv file was valid than a triggered event on the server gonna load the data into the database. Then all the statitistical calculation gonna happen on the run of the request
   1. request example:
      ```
      curl -X 'GET' \
      'http://127.0.0.1:8000/api/v1/statistics/ \
      -H 'accept: application/json' \
      -H 'X-CSRFToken: NyBYCU01QcQVsBn6M853zM5xhDBItC1LLApIP03pvW4U4xq8fDlzTDvm9mgxoFg8'
      ```
    1. response sample:
        ```
        {
          "count": 1,
          "next": null,
          "previous": null,
          "results": [
            {
              "aircraft": "S305A",
              "status": null,
              "type": null,
              "info_count": 17,
              "errors_count": 4,
              "pre_legend": 2,
              "warning": 0,
              "paired_b": 0,
              "legend": 4,
              "lower_b": 0,
              "repeat_legend": 0,
              "upper_a": 1,
              "lower_a": 0,
              "paired_a": 0
            },
            {
              "aircraft": "S306A",
              "status": null,
              "type": null,
              "info_count": 5,
              "errors_count": 9,
              "pre_legend": 1,
              "warning": 0,
              "paired_b": 0,
              "legend": 1,
              "lower_b": 0,
              "repeat_legend": 0,
              "upper_a": 0,
              "lower_a": 1,
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

## run test files
1. run all test files in the project
```
fab test.run
```
