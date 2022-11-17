from flask import Blueprint
from flask_restx import Namespace, Resource

from dtos.ErroDTO import ErroDTO
from dtos.ResponseDTO import ResponseDTO

from alocators.AlocatorUFC import AlocatorUFC

alocator_controller = Blueprint("alocator_controller", __name__)

namespace_alocator = Namespace('Alocador', description="Criar a alocação")

@namespace_alocator.route('/alocator', methods=['POST'])
class AlocatorController(Resource):
    @staticmethod
    @namespace_alocator.doc(responses={200: "Alocação concluida com sucesso."})
    @namespace_alocator.doc(responses={400: "Parâmetros de entrada inválidos."})
    @namespace_alocator.doc(responses={500: "Falha ao executar esse procedimento, por favor tente novamente."})
    def post():
        try:
            alocator = AlocatorUFC()
            alocator.alocar_horarios()
            return ResponseDTO("Alocação concluida com sucesso.", 200).response()
        except Exception as e:
            return ErroDTO(str(e)).response()