from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask('app')
app.config.from_object('app.config')
db = SQLAlchemy(app)
Bootstrap(app)

from app import views, models
