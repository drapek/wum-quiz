#!flask/bin/python
import sys
from app import app

app.run(debug=True, port=80)
