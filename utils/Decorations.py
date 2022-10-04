from functools import wraps

from flask import request, Response

import jwt

from database.models.Usuario import Usuario
from dtos.ErroDTO import ErroDTO
from dtos.ResponseDTO import ResponseDTO
from services import JWTService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers

        if not 'Authorization' in headers:
            return ResponseDTO("É necessário um token para essa requisição", 400).response()

        try:
            #pegando token do headers
            token = str(headers["Authorization"].replace('Bearer ', '')).strip()

            user_id = JWTService.decode(token)

            current_user = Usuario.select().where(Usuario.id == user_id).get()

        except jwt.ExpiredSignatureError:
            return ResponseDTO("Token expirado.", 401).response()
        except jwt.InvalidTokenError:
            return ResponseDTO("Token inválido.", 401).response()
        except Exception:
            raise ErroDTO().response()

        return f(current_user, *args, **kwargs)
    return decorated