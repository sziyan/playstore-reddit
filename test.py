from app.models import Games,Apps
from app import session

app = Apps(title='Whatsapp', link='https://store.google.com/whatsapp',count=3)
session.add(app)
session.commit()

