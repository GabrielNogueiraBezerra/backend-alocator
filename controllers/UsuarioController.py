import json

from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioBaseDTO
from utils import Decorations

usuario_controller = Blueprint('usuario_controller', __name__)

api = Namespace('Usuário')

user_fields = api.model('usuarioBaseDTO', {'nome': fields.String, 'email': fields.String})

@api.route('/', methods=["GET"])
class UsuarioController(Resource):
    @api.doc(responses={200: "Consulta completa."})
    @api.doc(responses={401: "Token inválido ou Expirado."})
    @api.doc(security='apikey')
    @api.response(200, "Sucess", user_fields)
    @Decorations.token_required
    def get(self, current_user):
        try:
            return Response(
                json.dumps(UsuarioBaseDTO("teste", "login_teste").__dict__),
                status=200,
                mimetype='application/json')
        except Exception as e:
            return Response(
                json.dumps(ErroDTO("Não foi possível buscar usuarios, por favor tente novamente." + str(e), 500).__dict__),
                status=500,
                mimetype='application/json')