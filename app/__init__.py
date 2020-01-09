from config import Config
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


from app import models