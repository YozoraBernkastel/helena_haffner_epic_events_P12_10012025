import bcrypt
from peewee import *
from datetime import datetime

db = SqliteDatabase("database")


class Collaborator(Model):
    username = CharField(max_length=150) # todo unique = true ? ??
    password = BitField()
    role = CharField()

    @staticmethod
    def dress_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=bytes(password, encoding="ascii"), salt=salt)
        return hashed

    @classmethod
    def create_collab(cls, username: str, password: str, role: str) -> None:
        new_password = cls.dress_password(password)
        Collaborator.create(username=username, password=new_password, role=role)

    @classmethod
    def find_collaborator(cls, username, password) -> object | None:
        user = cls.get_or_none(username=username)
        password = bytes(password, encoding="ascii")

        if user is not None and bcrypt.checkpw(password, user.password):
            return user

        return None

    def update_username(self, new_username: str) -> None:
        self.username = new_username
        self.save()

    def update_password(self, new_password: str) -> None:
        new_password = self.dress_password(new_password)
        self.password = new_password
        self.save()

    def update_role(self, new_role: str):
        self.role = new_role
        self.save()

    @classmethod
    def find_last_user_session(cls, user_id: int) -> object | None:
        user = cls.get_or_none(id=user_id)

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
