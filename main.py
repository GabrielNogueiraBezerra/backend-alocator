from flask import Flask
from flask_restx import Api

import config
from controllers.LoginController import login_controller
from controllers.ProfessorController import professor_controller
from controllers.UsuarioController import usuario_controller

from controllers.LoginController import api as ns_login
from controllers.ProfessorController import api as ns_professor
from controllers.UsuarioController import api as ns_usuario

app = Flask(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Digite na caixa de entrada *'Value'* abaixo: **'Bearer &lt;JWT&gt;'**, onde JWT é o token"
    }
}

api = Api(app,
          config.API_VERSION,
          config.API_TITLE,
          config.API_DESCRIPTION,
          doc='/docs',
          authorizations=authorizations,
          security='apikey'
          )

def register_blueprints():
    app.register_blueprint(login_controller, url_prefix=config.API_BASE_URL)
    app.register_blueprint(usuario_controller, url_prefix=config.API_BASE_URL+'/usuario')
    app.register_blueprint(professor_controller, url_prefix=config.API_BASE_URL)

def add_namespaces():
    api.add_namespace(ns_login, path=config.API_BASE_URL)
    api.add_namespace(ns_usuario, path=config.API_BASE_URL+'/usuario')
    api.add_namespace(ns_professor, path=config.API_BASE_URL)


if __name__ == '__main__':
    register_blueprints()
    add_namespaces()

    print(config.SECRET_KEY)

    app.run(host=config.API_HOST,
            port=config.API_PORT,
            debug=config.DEBUG)
