from dtos.ResponseDTO import ResponseDTO


class UsuarioDTO(ResponseDTO):
    def __init__(self, nome, email, token):
        self.nome = nome
        self.email = email
        self.token = token
        super().__init__("Login efetuado com sucesso.", 200)