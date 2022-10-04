from peewee import TextField
from database.models.BaseModel import BaseModel


class Usuario(BaseModel):
    nome = TextField()
    email = TextField()
    senha = TextField()


Usuario.create_table()
