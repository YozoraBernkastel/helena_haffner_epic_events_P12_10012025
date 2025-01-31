import bcrypt
from peewee import *
from datetime import datetime
from Helper.jwt_helper import JwtHelper

db = SqliteDatabase("database")

class Collaborator(Model):
    username = CharField(max_length=150)
    password = BitField()
    role = CharField()

    @classmethod
    def find_collaborator(cls, username, password) -> object | None:
        user = cls.get_or_none(username=username)
        password = bytes(password, encoding="ascii")

        if user is not None and bcrypt.checkpw(password, user.password):
            return user

        return None

    @classmethod
    def find_last_user_session(cls, user_id: str) -> object | None:
        user = cls.get_or_none(id=int(user_id))

        if user is not None:
            return user

        return None

    class Meta:
        database = db

class Client(Model):
    full_name = CharField(max_length=150)
    mail = CharField()
    tel = CharField()
    company_name = CharField(max_length=150)
    creation_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())
    collaborator_id = ForeignKeyField(Collaborator, backref="clients")
    information = CharField()

    class Meta:
        database = db


class Contract(Model):
    client_id = ForeignKeyField(Client, backref="contracts")
    collaborator = ForeignKeyField(Collaborator, backref="contracts")
    total_value = DoubleField()
    remains_to_be_paid = DoubleField()
    signed = BooleanField()
    creation_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = db

class Event(Model):
    name = CharField()
    contract = ForeignKeyField(Contract, backref="events")
    client = ForeignKeyField(Client, backref="events")
    starting_time = DateTimeField()
    ending_time = DateTimeField()
    support = ForeignKeyField(Collaborator, backref="support_events")
    address = CharField()
    attendant_number = IntegerField()
    comment = CharField()

    class Meta:
        database = db
