from django.http import HttpRequest, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from stackoverflow.settings import SECRET_KEY
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return datetime.strftime(o, "%m/%d/%Y")

        return json.JSONEncoder.default(self, o)

def check_token(req: HttpRequest):
    if req.headers.get('token', '') == SECRET_KEY:
        return True
    return False

def positive_response(data):
    Json = {
        'status': 'ok',
        'data': data
    }
    return json.dumps(Json, cls=DateTimeEncoder)

def negative_response(message):
    Json = {
        'status': 'error',
        'message': message
    }
    return json.dumps(Json, cls=DateTimeEncoder)

def to_dict(instance):
    data = instance.__dict__.copy()
    keys = []
    for key in data.keys():
        if key.startswith('_'):
            keys.append(key)
    for key in keys:
        data.pop(key)
    return data