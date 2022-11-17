from peewee import *
from enum import Enum
import os

db = SqliteDatabase('banco.db')

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    nome = TextField()
    email = TextField()
    senha = TextField()

class Periodo(BaseModel):
    descricao = TextField()

class Horario(BaseModel):
    periodo = ForeignKeyField(Periodo, backref='periodos', column_name='id_periodo', null=True)
    dia = IntegerField()

class Curso(BaseModel):
    nome = TextField()

class Dia(Enum):
    SEGUNDA = 1
    TERCA = 2
    QUARTA = 3
    QUINTA = 4
    SEXTA = 5
    SABADO = 6
    DOMING = 7


db.connect()
db.create_tables([Usuario, Periodo, Horario, Curso])
db.close()