from flask import Flask
from flask_restx import Api

import config

from controllers.ProfessorController import professor_controller

from controllers.ProfessorController import api as ns_professor

app = Flask(__name__)

api = Api(app,
          config.API_VERSION,
          config.API_TITLE,
          config.API_DESCRIPTION,
          doc='/docs'
          )

def register_blueprints():
    app.register_blueprint(professor_controller, url_prefix=config.API_BASE_URL)

def add_namespaces():
    api.add_namespace(ns_professor, path=config.API_BASE_URL)

if __name__ == '__main__':
    register_blueprints()
    add_namespaces()

    app.run(host=config.API_HOST,
            port=config.API_PORT,
            debug=config.DEBUG)
