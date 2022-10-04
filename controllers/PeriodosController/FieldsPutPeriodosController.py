from interfaces.fields import Fields
from flask_restx import fields

class FieldsPutPeriodosController(Fields):
    def __init__(self, namespace):
        super().__init__(namespace)

    def inputs(self):
        return self.namespace.model("input_periodo", {"id": fields.Integer, "descricao": fields.String})

    def outputs(self):
        pass