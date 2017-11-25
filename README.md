# QUIZ WUM

## Introduction

This is app to help memorize latin names of bacteria. It is deployed on heroku under this
address: [heroku_link:](https://wum-quiz.herokuapp.com/)

## Installation
1) Install the required packages
```bash
pip install -r requriements.txt
```
2) Init the database 
(using Python console)
```python
from app.functions import db_create
db_create()
```
3) Read initial data from example_data folder (using Python console)
```python
from app.functions import import_csv_data
import_csv_data('example_data/import_data.csv')
```
## Requirements
* Python 3.6
* Flask 0.12.2