from datetime import datetime
from app import db


class Url(db.Document):
    long_url = db.StringField(max_length=255, required=True, unique=True)
    short_url = db.StringField(max_length=255, required=True)
    created = db.DateTimeField(default=datetime.now, required=True)
    visits = db.IntField(default=0, required=True)
