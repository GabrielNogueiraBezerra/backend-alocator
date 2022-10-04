from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

from controllers.LoginController.FieldsLoginController import FieldsLoginController
from database.models.Usuario import Usuario

from dtos.ErroDTO import ErroDTO
from dtos.ResponseDTO import ResponseDTO
from dtos.UsuarioDTO import UsuarioDTO
from services import JWTService

login_controller = Blueprint("login_controller", __name__)

namespace_login = Namespace('Login', description="Realizar login na aplicação")

fields_post = FieldsLoginController(namespace_login)

@namespace_login.route('/login', methods=['POST'])
class LoginController(Resource):
    @staticmethod
    @namespace_login.doc(responses={200: "Login efetuado com sucesso."})
    @namespace_login.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_login.doc(responses={401: "Usuário ou Senha incorretos."})
    @namespace_login.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_login.expect(fields_post.inputs())
    @namespace_login.response(200, "Login efetuado com sucesso.", fields_post.outputs())
    def post():
        try:
            body = request.get_json()

            if (not body) or ("login" not in body) or ("senha" not in body):
                return ResponseDTO("Parâmetros de entrada inválidos.", 400).response()

            usuario = Usuario.select().where(Usuario.email == body["login"] and Usuario.senha == body["senha"]).get()

            if usuario:
                token = JWTService.encode(usuario.id)
                return UsuarioDTO(usuario.nome, usuario.email, token).response()

            return ResponseDTO("Usuário ou Senha incorretos, por favor tente novamente.", 401).response()
        except Exception as e:
            return ErroDTO(str(e)).response()