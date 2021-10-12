import json
from core.models import User, Question, Answer, Tag
from django.core.serializers import serialize
from django.http import QueryDict

ENCODING = 'utf-8'
FORMAT = 'json'


class UserJson:
    def __init__(self, raw_json):
        self.json = json.loads(raw_json.decode(ENCODING))
        self.username = self.json.get('username', None)
        self.password = self.json.get('password', None)
        self.img_path = self.json.get('img_path', None)
        self.location = self.json.get('location', None)
        self.title = self.json.get('title', None)
        self.about = self.json.get('about', None)
        self.reputation = self.json.get('reputation', None)
        self.questions = self.json.get('questions', None)
        self.answers = self.json.get('answers', None)
        self.created = self.json.get('created', None)


class QuestionJson:
    def __init__(self, raw_json):
        self.json = json.loads(raw_json.decode(ENCODING))
        self.title = self.json.get('title', None)
        self.votes = self.json.get('votes', None)
        self.views = self.json.get('views', None)
        self.text = self.json.get('body', None)
        self.tags = self.json.get('tags', None)
        self.user = self.json.get('user', None)
        self.answers = self.json.get('answers', None)
        self.created = self.json.get('created', None)


class AnswerJson:
    def __init__(self, raw_json):
        self.json = json.loads(raw_json.decode(ENCODING))
        self.text = self.json.get('text', None)
        self.likes = self.json.get('likes', None)
        self.question = self.json.get('question', None)
        self.user = self.json.get('user', None)
        self.created = self.json.get('created', None)


class TagJson:
    def __init__(self, raw_json):
        self.json = json.loads(raw_json.decode(ENCODING))
        self.name = self.json.get('name', None)
        self.count = self.json.get('count', None)


class UrlParamsDict:
    def __init__(self, query_dict):
        self.filter_dict = {}
        self.order_by = None
        self.page = None
        for key in query_dict:
            if key not in ('order_by', 'page'):
                self.filter_dict[key] = query_dict[key]
            elif key == 'order_by':
                self.order_by = query_dict[key]
            elif key == 'page':
                self.page = query_dict[key]




















