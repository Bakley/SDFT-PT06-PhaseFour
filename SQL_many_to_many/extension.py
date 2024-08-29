from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

db = SQLAlchemy()
api = Api()
migrate = Migrate()
