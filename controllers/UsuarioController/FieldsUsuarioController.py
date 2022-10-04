from interfaces.fields import Fields
from flask_restx import fields

class FieldsUsuarioController(Fields):
    def __init__(self, namespace):
        super().__init__(namespace)

    def inputs(self):
        return self.namespace.model("input_usuario", {"nome": fields.String, "email": fields.String, "senha": fields.String})

    def outputs(self):
        pass