import json
from functools import wraps

from flask import request, Response

import jwt

from dtos.ErroDTO import ErroDTO
from dtos.UsuarioDTO import UsuarioBaseDTO
from services import JWTService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers

        if not 'Authorization' in headers:
            return Response(
                json.dumps(ErroDTO("É necessário um token para essa requisição", 400).__dict__),
                status=400,
                mimetype="application/json"
            )

        try:
            #pegando token do headers
            token = str(headers["Authorization"].replace('Bearer ', '')).strip()

            user_id = JWTService.decode(token)

            current_user = UsuarioBaseDTO('teste', "login_teste")

        except jwt.ExpiredSignatureError:
            return Response(
                json.dumps(ErroDTO("Token expirado", 401).__dict__),
                status=401,
                mimetype="application/json"
            )
        except jwt.InvalidTokenError:
            return Response(
                json.dumps(ErroDTO("Token inválido", 401).__dict__),
                status=401,
                mimetype="application/json"
            )
        except Exception:
            raise Response(
                json.dumps(ErroDTO("Não foi possível verificar o token", 500).__dict__),
                status=500,
                mimetype="application/json"
            )

        return f(current_user, *args, **kwargs)
    return decorated