import random
import string

API_VERSION = '1.0.0.0'
API_TITLE = 'alocate()'
API_DESCRIPTION = 'Aplicação de alocação de horários e salas'

API_HOST = '127.0.0.1'
API_PORT = 5000
API_BASE_URL = '/api'

#chave aleatoria para geração do JWT
SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits + string.ascii_uppercase) for i in range(32))

DEBUG = True