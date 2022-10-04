from dtos.ResponseDTO import ResponseDTO


class ErroDTO(ResponseDTO):
    def __init__(self, exception):
        super().__init__("Falha ao executar esse procedimento, por favor tente novamente.", 500)
        self.exception = exception