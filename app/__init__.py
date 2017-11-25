from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.config.from_object('app.config')
db = SQLAlchemy(app)


from app import views, models
