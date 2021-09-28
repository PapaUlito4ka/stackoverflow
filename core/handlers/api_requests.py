import requests
import json

from django.http import HttpRequest

from stackoverflow.settings import SECRET_KEY
from urllib.parse import urlencode

BASE_URL = 'http://localhost:8000/api/'
header = {
    'token': SECRET_KEY
}


class User:

    @staticmethod
    def create_user(username, password):
        url = BASE_URL + 'user/create'
        data = json.dumps({
            'username': username,
            'password': password
        })
        response = requests.post(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_users(url_params: dict):
        url_params_str = urlencode(url_params)
        url = BASE_URL + f'users?{url_params_str}'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user(username):
        url = BASE_URL + 'user/{}'.format(username)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_user(username, username_, password_):
        url = BASE_URL + 'user/{}'.format(username)
        data = json.dumps({
            'username': username_,
            'password': password_
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def delete_user(username):
        url = BASE_URL + 'user/{}'.format(username)
        response = requests.delete(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_username(username):
        url = BASE_URL + 'user/{}/username'.format(username)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_user_username(username, username_):
        url = BASE_URL + 'user/{}/username'.format(username)
        data = json.dumps({
            'username': username_
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_user_password(username, password_):
        url = BASE_URL + 'user/{}/password'.format(username)
        data = json.dumps({
            'password': password_
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_questions(username):
        url = BASE_URL + 'user/{}/questions'.format(username)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_answers(username):
        url = BASE_URL + 'user/{}/answers'.format(username)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=profile'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def post_user_profile(request: HttpRequest, username: str, filename: str):
        url = BASE_URL + f'user/{username}/profile'
        data = json.dumps({
            'img_path': filename,
            'username': request.POST.get('username'),
            'about': request.POST.get('about')
        })
        response = requests.post(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile_activity(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=activity'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile_edit(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=edit'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile_answers(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=answers'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile_questions(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=questions'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_user_profile_tags(username: str):
        url = BASE_URL + f'user/{username}/profile?tab=tags'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }


class Question:

    @staticmethod
    def create_question(title, body, tags, user):
        url = BASE_URL + 'question/create'
        data = json.dumps({
            'title': title,
            'body': body,
            'tags': tags,
            'user': user
        })
        response = requests.post(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_questions(params_str: str):
        url = BASE_URL + 'questions/?{}'.format(params_str)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question(id_):
        url = BASE_URL + 'question/{}'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_question(id_, text):
        url = BASE_URL + 'question/{}'.format(id_)
        data = json.dumps({
            'text': text
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def delete_question(id_):
        url = BASE_URL + 'question/{}'.format(id_)
        response = requests.delete(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_votes(id_):
        url = BASE_URL + 'question/{}/votes'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_question_votes(id_):
        url = BASE_URL + 'question/{}/votes'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_views(id_):
        url = BASE_URL + 'question/{}/views'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_question_views(id_):
        url = BASE_URL + 'question/{}/views'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_text(id_):
        url = BASE_URL + 'question/{}/text'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_question_text(id_, text):
        url = BASE_URL + 'question/{}/text'.format(id_)
        data = json.dumps({
            'text': text
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_tags(id_):
        url = BASE_URL + 'question/{}/tags'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_answers(id_):
        url = BASE_URL + 'question/{}/answers'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_question_user(id_):
        url = BASE_URL + 'question/{}/user'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def search_question(url_params: dict):
        url = BASE_URL + f'questions?{urlencode(url_params)}'
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }


class Answer:

    @staticmethod
    def create_answer(text, question_id, user_id):
        url = BASE_URL + 'answer/create'
        data = json.dumps({
            'text': text,
            'question': question_id,
            'user': user_id
        })
        response = requests.post(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_answer(id_):
        url = BASE_URL + 'answer/{}'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_answer(id_, text):
        url = BASE_URL + 'answer/{}'.format(id_)
        data = json.dumps({
            'text': text
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def delete_answer(id_):
        url = BASE_URL + 'answer/{}'.format(id_)
        response = requests.delete(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_answer_text(id_):
        url = BASE_URL + 'answer/{}/text'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_answer_text(id_, text):
        url = BASE_URL + 'answer/{}/text'.format(id_)
        data = json.dumps({
            'text': text
        })
        response = requests.get(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_answer_likes(id_):
        url = BASE_URL + 'answer/{}/likes'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_answer_likes(id_):
        url = BASE_URL + 'answer/{}/likes'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_answer_question(id_):
        url = BASE_URL + 'answer/{}/question'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_answer_user(id_):
        url = BASE_URL + 'answer/{}/user'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }


class Tag:

    @staticmethod
    def create_tag(name):
        url = BASE_URL + 'tag/create'
        data = json.dumps({
            'name': name
        })
        response = requests.post(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_tag(id_):
        url = BASE_URL + 'tag/{}'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_tag(id_, name):
        url = BASE_URL + 'tag/{}'.format(id_)
        data = json.dumps({
            'name': name
        })
        response = requests.put(url, headers=header, data=data)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def delete_tag(id_):
        url = BASE_URL + 'tag/{}'.format(id_)
        response = requests.delete(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_tag_count(id_):
        url = BASE_URL + 'tag/{}/count'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def put_tag_count(id_):
        url = BASE_URL + 'tag/{}/count'.format(id_)
        response = requests.put(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }

    @staticmethod
    def get_tag_questions(id_):
        url = BASE_URL + 'tag/{}/questions'.format(id_)
        response = requests.get(url, headers=header)
        return {
            'status_code': response.status_code,
            **response.json()
        }
