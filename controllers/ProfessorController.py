from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

from dtos.ErroDTO import ErroDTO

import json

professor_controller = Blueprint('professor_controller', __name__)

api = Namespace('Professor', description="Controle de professores")

professor_fields = api.model('professorDTO',
                             {'nome': fields.String}
                             )
@api.route('/professor', methods =['POST'])
class Professor(Resource):
    @api.doc(responses={200: "Professor cadastrado com sucesso."})
    @api.doc(responses={400: "Parâmetros de entrada inválidos."})
    @api.doc(responses={500: "Não foi possível cadastrar o professor, tente novamente."})
    @api.expect(professor_fields)
    def post(self):
        try:
            body = request.get_json()

            if (not body) or ("nome" not in body):
                return Response(json.dumps(ErroDTO("Parâmetros de entrada inválidos.", 400).__dict__),
                                status=400,
                                mimetype='application/json')



            return Response("Professor cadastrado com sucesso.",
                            status=200,
                            mimetype='application/json')
        except Exception as e:
            return Response(json.dumps(ErroDTO("Não foi possível cadastrar o professor, tente novamente.", 500).__dict__),
                                status=500,
                                mimetype='application/json')
