import bcrypt
from peewee import *
from datetime import datetime

db = SqliteDatabase("database")


class Collaborator(Model):
    username = CharField(max_length=150, unique=True)
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


class Customer(Model):
    full_name = CharField(max_length=150)
    mail = CharField(unique=True)
    phone = CharField()
    company_name = CharField(max_length=150)
    creation_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())
    collaborator = ForeignKeyField(Collaborator, backref="customers")
    information = CharField()

    class Meta:
        database = db


class Contract(Model):
    name = CharField(unique=True)
    customer = ForeignKeyField(Customer, backref="contracts")
    collaborator = ForeignKeyField(Collaborator, backref="contracts")
    total_value = DoubleField()
    remains_to_be_paid = DoubleField()
    signed = BooleanField(default=False)
    creation_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = db

class Event(Model):
    name = CharField(unique=True)
    contract = ForeignKeyField(Contract, backref="events")
    starting_time = DateTimeField()
    ending_time = DateTimeField()
    support = ForeignKeyField(Collaborator, backref="support_events", null=True)
    address = CharField()
    attendant_number = IntegerField()
    comment = CharField()

    class Meta:
        database = db


# charfield, textifield, imagefield, filefield et emailfield ne peuvent pas être null !!