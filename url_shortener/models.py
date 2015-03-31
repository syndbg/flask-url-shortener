from datetime import datetime
from app import db


class Url(db.Document):
    long_url = db.StringField(max_length=255, required=True, unique=True)
    short_url = db.StringField(max_length=255, required=True)
    created = db.DateTimeField(default=datetime.now, required=True)
    visits = db.IntField(default=0, required=True)

    @staticmethod
    def has_all_required_fields(cls, given_fields):
        given_fields = given_fields.keys()
        required_fields = cls.get_required_fields()
        return all(required in given_fields for required in required_fields)

    @staticmethod
    def has_any_required_fields(cls, given_fields):
        given_fields = given_fields.keys()
        required_fields = cls.get_required_fields()
        return any(required in given_fields for required in required_fields)

    @staticmethod
    def get_required_fields(cls):
        return [key for key, value in cls._fields.iteritems() if value.required]

    def update_fields(self, given_pairs):
        required_fields = self.get_required_fields()
        for field, value in given_pairs.iteritems():
            if field in required_fields:
                setattr(self, field, value)
