from flask import Blueprint, request, Response
from flask_restx import Namespace, Resource, fields

from controllers.UsuarioController.FieldsUsuarioController import FieldsUsuarioController
from database.models.Usuario import Usuario

from dtos.ErroDTO import ErroDTO
from dtos.ResponseDTO import ResponseDTO

from utils import decorations

usuario_controller = Blueprint("usuario_controller", __name__)

namespace_usuario = Namespace('Usuario', description="Manter dados de usuários")

fields_post = FieldsUsuarioController(namespace_usuario)

@namespace_usuario.route('/usuario', methods=['POST'])
class UsuarioController(Resource):
    @staticmethod
    @namespace_usuario.doc(responses={200: "Usuário cadastrado com sucesso."})
    @namespace_usuario.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_usuario.doc(responses={409: "Já existe um usuário com esse email cadastrado."})
    @namespace_usuario.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    @namespace_usuario.expect(fields_post.inputs())
    @namespace_usuario.doc(security='apikey')
    @decorations.token_required
    def post(current_user):
        try:
            body = request.get_json()

            if (not body) or ("nome" not in body) or ("email" not in body) or ("senha" not in body):
                return ResponseDTO("Parâmetros de entrada inválidos.", 400).response()

            RowExisting = True

            try:
                Usuario.select().where(Usuario.email == str(body["email"])).get()
            except Usuario.DoesNotExist:
                RowExisting = False

            if RowExisting:
                return ResponseDTO("Já existe um usuário com esse email cadastrado.", 409).response()

            Usuario.create(
                nome=body["nome"],
                email=body["email"],
                senha=body["senha"]
            )

            return ResponseDTO("Usuário cadastrado com sucesso.", 400).response()
        except Exception as e:
            return ErroDTO(str(e)).response()