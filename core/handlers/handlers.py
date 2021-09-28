import requests
import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from core.handlers.api_requests import User, Question, Tag, Answer
from stackoverflow.settings import SECRET_KEY

ERROR_STATUS = 403


def make_session(request: HttpRequest, response: dict, context: dict):
    request.session['id'] = response['data']['id']
    request.session['username'] = response['data']['username']
    context['session'] = request.session


def check_error(response: dict):
    return response['status_code'] == ERROR_STATUS


def handle_error(request: HttpRequest, url: str, response: dict, context: dict):
    context['error'] = response['message']
    return render(request, url, context=context)


def check_user_password(response: dict, pwd: str):
    return response['data']['password'] == pwd


def handle_response(request: HttpRequest, url: str, response: dict, context: dict):
    context = {
        **context,
        **response['data']
    }
    return render(request, url, context=context)


def handle_question(request: HttpRequest, url: str, response: dict, context: dict):
    context['question'] = response['data']
    return render(request, url, context=context)


def handle_questions(request: HttpRequest, url: str, response: dict, context: dict):
    context['questions'] = response['data']
    return render(request, url, context=context)


def handle_uploaded_file(f, filename: str):
    with open(f'/Users/viktormartahin/Documents/Projects/stackoverflow/static/images/{filename}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
