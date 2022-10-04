from interfaces.fields import Fields
from flask_restx import fields

class FieldsLoginController(Fields):
    def __init__(self, namespace):
        super().__init__(namespace)

    def inputs(self):
        return self.namespace.model("input_login", {"login": fields.String, "senha": fields.String})

    def outputs(self):
        return self.namespace.model("output_login", {"nome": fields.String, "email": fields.String, "token": fields.String})