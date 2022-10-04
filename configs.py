#Api Descriptions
import string
import random

API_VERSION = '1.0.0'
API_TITLE = "alocate()"
API_DESCRIPTION = 'Aplicação de alocação de horários e salas'

#Api configurations
API_HOST = "127.0.0.1"
API_PORT = 5000
API_BASE_URL = '/api'
API_DEBUG = True
API_RANDOM_CRT = string.ascii_letters + string.digits + string.ascii_uppercase
API_SECRET_KEY = 'SECRET'
API_SECRET_KEY_2 = ''.join(random.choice(API_RANDOM_CRT) for i in range(32))

#Api configurations documentations
API_AUTHORIZATIONS = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Digite na caixa de entrada *'Value'* abaixo: **'Bearer &lt;JWT&gt;'**, onde JWT é o token"
    }
}
API_BASE_URL_DOCS = '/docs'
API_SECURITY = 'apikey'