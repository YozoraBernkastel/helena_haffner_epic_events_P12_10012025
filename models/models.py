from peewee import *
from datetime import datetime

db = SqliteDatabase("database")

class Collaborator(Model):
    username = CharField(max_length=150)
    # todo ne pas oublier de crypter le mot de passe avant de l'envoyer en bdd !!!!!!!!!
    password = CharField()
    role = CharField()

    # todo créer des fonctions liées au model (par exemple create, modif, etc) --
    #  des classMethod par exemple) pour facilter le code puisqu'on a tout au même endroit. Facilite notamment les choses lorsqu'on passe via le terminal !!

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

    # todo regarder récap mentorat !!!

    # todo quelle architecture utiliser ? MVC ??? Chercher autres possibilités histoire de se renseigner même si MVC
    # todo surement mieux et plus simple (voir projet 4)

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
