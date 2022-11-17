import json

from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, reqparse

from controllers.PeriodosController.FieldsPeriodosController import FieldsPeriodosController
from controllers.PeriodosController.FieldsPutPeriodosController import FieldsPutPeriodosController
from DB import Periodo

from dtos.ErroDTO import ErroDTO
from dtos.PeriodoDTO import PeriodoDTO
from dtos.ResponseDTO import ResponseDTO

from utils import decorations

periodo_controller = Blueprint("periodo_controller", __name__)

namespace_periodo = Namespace('Periodos', description="Manter dados de periodos")

fields = FieldsPeriodosController(namespace_periodo)
fields_put = FieldsPutPeriodosController(namespace_periodo)

parser = reqparse.RequestParser()
parser.add_argument('id_periodo', type=int, help='Id do periodo')


@namespace_periodo.route('/periodo', methods=['POST', 'GET', 'PUT', 'DELETE'])
class PeriodosController(Resource):
    @staticmethod
    @namespace_periodo.doc(responses={200: "Periodo cadastrado com sucesso."})
    @namespace_periodo.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_periodo.doc(responses={409: "Já existe um periodo com essa descrição cadastrada."})
    @namespace_periodo.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_periodo.expect(fields.inputs())
    @namespace_periodo.doc(security='apikey')
    @decorations.token_required
    def post(current_user):
        try:
            body = request.get_json()

            if (not body) or ("descricao" not in body):
                return ResponseDTO("Parâmetros de entrada inválidos.", 400).response()

            RowExisting = True

            try:
                Periodo.select().where(Periodo.descricao == body["descricao"]).get()
            except Periodo.DoesNotExist:
                RowExisting = False

            if RowExisting:
                return ResponseDTO("Já existe uma periodo com essa descrição cadastrada.", 409).response()

            Periodo.create(
                descricao=body["descricao"],
            )

            return ResponseDTO("Periodo cadastrado com sucesso.", 400).response()
        except Exception as e:
            return ErroDTO(str(e)).response()

    @staticmethod
    @namespace_periodo.doc(parser=parser)
    @namespace_periodo.doc(responses={200: "Periodo(s) resgatado(s) com sucesso."})
    @namespace_periodo.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_periodo.doc(responses={409: "Nenhum periodo com esse id encontrado."})
    @namespace_periodo.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_periodo.doc(security='apikey')
    @namespace_periodo.response(200, "Sucess", [fields.outputs()])
    @decorations.token_required
    def get(current_user):
        try:
            id = request.args.get('id_periodo')

            if id:
                try:
                    periodo = Periodo.select().where(Periodo.id == id).get()
                    return PeriodoDTO(periodo.id, periodo.descricao).response()
                except Periodo.DoesNotExist:
                    return ResponseDTO("Nenhum periodo com esse id encontrado.", 409).response()

            periodos = []
            query = Periodo.select().dicts()
            for row in query:
                periodos.append(row)

            return Response(json.dumps(periodos), 200, mimetype="application/json")
        except Exception as e:
            return ErroDTO(str(e)).response()

    @staticmethod
    @namespace_periodo.expect(fields_put.inputs())
    @namespace_periodo.doc(responses={200: "Periodo alterado com sucesso."})
    @namespace_periodo.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_periodo.doc(responses={409: "Nenhum periodo com esse id encontrado."})
    @namespace_periodo.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_periodo.doc(security='apikey')
    @decorations.token_required
    def put(current_user):
        try:
            body = request.get_json()

            if (not body) or ("id" not in body) or ("descricao" not in body):
                return ResponseDTO("Parâmetros de entrada inválidos.", 400).response()

            try:
                Periodo.select().where(Periodo.id == body["id"]).get()
            except Periodo.DoesNotExist:
                return ResponseDTO("Nenhum periodo com esse id encontrado.", 409).response()

            res = (Periodo
                   .update(descricao=body["descricao"])
                   .where(Periodo.id == body["id"])
                   .execute())

            return ResponseDTO("Periodo alterado com sucesso", 200).response()

        except Exception as e:
            return ErroDTO(str(e)).response()

    @staticmethod
    @namespace_periodo.doc(parser=parser)
    @namespace_periodo.doc(responses={200: "Periodo excluido com sucesso."})
    @namespace_periodo.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_periodo.doc(responses={409: "Nenhum periodo com esse id encontrado."})
    @namespace_periodo.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_periodo.doc(security='apikey')
    @decorations.token_required
    def delete(current_user):
        try:
            id = request.args.get('id_periodo')

            if id:
                try:
                    periodo = Periodo.select().where(Periodo.id == id).get()

                    Periodo.delete().where(Periodo.id == id).execute()

                    return ResponseDTO('Periodo excluido com sucesso.', 200).response()
                except Periodo.DoesNotExist:
                    return ResponseDTO("Nenhum periodo com esse id encontrado.", 409).response()

            return ResponseDTO("Parâmetros de entrada inválidos.", 400).response()
        except Exception as e:
            return ErroDTO(str(e)).response()