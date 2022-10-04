from flask import Response
import json

class ResponseDTO:
    def __init__(self, description, status):
        self.description = description
        self.status = status

    def response(self):
        return Response(json.dumps(self.__dict__), self.status, mimetype="application/json")