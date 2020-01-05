from config import Config
import sqlalchemy as db

engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

from app import models
