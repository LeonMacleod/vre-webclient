from flask import Flask;
from config import Config;
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate;


app = Flask(__name__)
#accessing configuration object from config.py
app.config.from_object(Config)
db = SQLAlchemy(app)

if __name__ == "__main__" :
    app.run()

from app import routes, models

