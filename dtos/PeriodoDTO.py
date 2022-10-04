from dtos.ResponseDTO import ResponseDTO


class PeriodoDTO(ResponseDTO):
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao
        super().__init__("Periodo(s) resgatado(s) com sucesso.", 200)