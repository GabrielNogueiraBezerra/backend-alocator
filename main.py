from flask import Flask

import configs

from documentation import Documentation

app = Flask(__name__)

if __name__ == '__main__':

    #iniciando a classe de documentação da API
    documentation = Documentation(app)
    documentation.init_class()

    #iniciando o serviço da API
    if configs.API_DEBUG:
        app.run(host=configs.API_HOST, port=configs.API_PORT, debug=True)
    else:
        from waitress import serve
        serve(app, host=configs.API_HOST, port=configs.API_PORT)


