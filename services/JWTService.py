import datetime

import jwt

import config


def encode(id_usuario):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1, minutes=0),
            'id_usuario': id_usuario
        }

        return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
    except Exception:
        pass

def decode(token):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithm="HS256")

        return payload["id_usuario"]
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError
    except Exception:
        raise Exception