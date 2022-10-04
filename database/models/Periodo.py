from peewee import TextField
from database.models.BaseModel import BaseModel


class Periodo(BaseModel):
    descricao = TextField()


Periodo.create_table()
