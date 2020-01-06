from app.models import Base
from app import engine

print('Database updated')
Base.metadata.create_all(engine)