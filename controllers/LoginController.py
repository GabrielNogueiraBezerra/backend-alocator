from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

from dtos.ErroDTO import ErroDTO

import json

from dtos.UsuarioDTO import UsuarioLoginDTO
from services import JWTService

login_controller = Blueprint('login_controller', __name__)

api = Namespace('Login', description="Login")

login_fields = api.model('loginDTO', {'usuario': fields.String,
                                      'senha': fields.String})

user_fields = api.model('usuarioDTO', {'nome': fields.String, 'email': fields.String, 'token': fields.String})

@api.route('/login', methods =['POST'])
class Login(Resource):
    @api.doc(responses={200: "Login efetuado com sucesso."})
    @api.doc(responses={400: "Parâmetros de entrada inválidos."})
    @api.doc(responses={500: "Não foi possível realizar o login, por favor tente novamente."})
    @api.response(200, "Sucess", user_fields)
    @api.expect(login_fields)
    def post(self):
        try:
            body = request.get_json()

            if (not body) or ("usuario" not in body) or ("senha" not in body):
                return Response(json.dumps(ErroDTO("Parâmetros de entrada inválidos.", 400).__dict__),
                                status=400,
                                mimetype='application/json')

            if body["usuario"] == "login_teste" and body["senha"] == "senha_teste":
                id_usuario = 1
                token = JWTService.encode(id_usuario)
                return Response(
                                json.dumps(UsuarioLoginDTO("teste", "login_test", token).__dict__),
                                status=200,
                                mimetype='application/json')

            return Response(json.dumps(ErroDTO("Usuário ou Senha incorretos, por favor tente novamente.", 401).__dict__),
                            status=401,
                            mimetype='application/json')


        except Exception as e:
            return Response(json.dumps(ErroDTO("Não foi possível realizar o login, por favor tente novamente.", 500).__dict__),
                                status=500,
                                mimetype='application/json')