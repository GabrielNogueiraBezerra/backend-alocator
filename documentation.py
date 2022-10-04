from flask_restx import Api

import configs

from controllers.LoginController.LoginController import login_controller, namespace_login
from controllers.UsuarioController.UsuarioController import usuario_controller, namespace_usuario
from controllers.PeriodosController.PeriodosController import periodo_controller, namespace_periodo

class Documentation:
    def __init__(self, app):
        self._app = app
        self._base_url = configs.API_BASE_URL
        self._api = Api(self._app,
                        configs.API_VERSION,
                        configs.API_TITLE,
                        configs.API_DESCRIPTION,
                        doc=configs.API_BASE_URL_DOCS,
                        authorizations=configs.API_AUTHORIZATIONS,
                        security=configs.API_SECURITY)

    def _registers_blueprints(self):
        self._app.register_blueprint(login_controller, url_prefix=self._base_url)
        self._app.register_blueprint(usuario_controller, url_prefix=self._base_url)
        self._app.register_blueprint(periodo_controller, url_prefix=self._base_url)

    def _add_namespaces(self):
        self._api.add_namespace(namespace_login, path=self._base_url)
        self._api.add_namespace(namespace_usuario, path=self._base_url)
        self._api.add_namespace(namespace_periodo, path=self._base_url)

    def init_class(self):
        self._registers_blueprints()
        self._add_namespaces()
