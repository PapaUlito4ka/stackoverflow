import requests
import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from core.handlers.api_requests import User, Question, Tag, Answer
from stackoverflow.settings import SECRET_KEY

from urllib.parse import urlencode

from core.handlers.handlers import *


class UserRequests:

    @staticmethod
    def login_user(request: HttpRequest, context, username, password):
        response = User.get_user(username)
        if check_error(response):
            return handle_error(request, 'core/login.html', response, context)
        if check_user_password(response, password):
            make_session(request, response, context)
            return redirect(f'/profile/{username}')
        return handle_error('core/login.html', context)

    @staticmethod
    def user_profile(request: HttpRequest, context, username):
        if request.method == 'POST':
            User.post_user_profile(request, username, context['filename'])
        response = User.get_user_profile(username)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/profile.html', response, context)

    @staticmethod
    def user_profile_activity(request: HttpRequest, context, username):
        response = User.get_user_profile_activity(username)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/activity.html', response, context)

    @staticmethod
    def user_profile_edit(request: HttpRequest, context, username):
        response = User.get_user_profile_edit(username)
        context['form'].fields['username'].initial = response['data']['user']['username']
        context['form'].fields['about'].initial = response['data']['user']['about']
        context['form'].fields['img_file'].initial = response['data']['user']['img_path']
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/edit.html', response, context)

    @staticmethod
    def user_profile_answers(request: HttpRequest, context, username):
        response = User.get_user_profile_answers(username)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/answers.html', response, context)

    @staticmethod
    def user_profile_questions(request: HttpRequest, context, username):
        response = User.get_user_profile_questions(username)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/questions.html', response, context)

    @staticmethod
    def user_profile_tags(request: HttpRequest, context, username):
        response = User.get_user_profile_tags(username)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/profile/tags.html', response, context)

    @staticmethod
    def register_user(request: HttpRequest, context, username, password):
        response = User.create_user(username, password)
        if check_error(response):
            return handle_error(request, 'core/register.html', response, context)
        make_session(request, response, context)
        return redirect(f'/profile/{username}')

    @staticmethod
    def get_user_questions(username):
        return User.get_user_questions(username)['data'][0]

    @staticmethod
    def get_users(request: HttpRequest, context: dict, url_params: dict):
        response = User.get_users(url_params)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/users.html', response, context)


class QuestionRequests:

    @staticmethod
    def get_question(request: HttpRequest, context, id_):
        response = Question.get_question(id_)
        Question.put_question_views(id_)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_question(request, 'core/question.html', response, context)

    @staticmethod
    def get_recent_questions(request: HttpRequest, context, url_params: dict):
        params_str = urlencode(url_params)
        response = Question.get_questions(params_str)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_questions(request, 'core/questions.html', response, context)

    @staticmethod
    def ask_question(request: HttpRequest, title, body, tags, user_id, context):
        response = Question.create_question(title, body, tags, user_id)
        if check_error(response):
            return handle_error(request, 'core/ask_question.html', response, context)
        return redirect(f'/profile/{request.session.get("username")}')

    @staticmethod
    def home_page(request: HttpRequest, context: dict, url_params: dict):
        params_str = urlencode(url_params)
        response = Question.get_questions(params_str)
        if check_error(response):
            return handle_error(request, 'base.html', response, context)
        return handle_questions(request, 'base.html', response, context)

    @staticmethod
    def search_question(request: HttpRequest, context: dict, url_params: dict):
        response = Question.search_question(url_params)
        if check_error(response):
            return handle_error(request, 'core/not_found.html', response, context)
        return handle_response(request, 'core/search.html', response, context)

class AnswerRequests:

    @staticmethod
    def create_answer(request: HttpRequest, context: dict, text: str, question_id: int, user_id: int):
        response = Answer.create_answer(text, question_id, user_id)
        if check_error(response):
            handle_error(request, 'core/question.html', response, context)
        return redirect(f'/question/{question_id}')


class TagRequests:

    @staticmethod
    def create_tag(request: HttpRequest, context: dict, tag_name: str):
        pass

    @staticmethod
    def get_tag(request: HttpRequest, context: dict, tag_name: str):
        pass










