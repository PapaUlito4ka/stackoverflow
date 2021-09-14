from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, QuestionForm, AnswerForm
from django.contrib import messages

import core.handlers.responses as handlers
from core.tests import QUESTIONS

QUESTION_FILTERS = {
    'Newest': 'created_at',
    'Oldest': '-created_at',
    'MostVotes': '-votes',
    'MostFrequent': '-views'
}


def home(request: HttpRequest):
    context = {
        'session': request.session
    }
    url_params = {
        'page': request.GET.get('page', 0)
    }
    return handlers.QuestionRequests.home_page(request, context, url_params)


@csrf_exempt
def login(request: HttpRequest):
    form = LoginForm()
    context = {
        'session': request.session,
        'form': form,
        'error': False
    }
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        return handlers.UserRequests.login_user(request, context, username, password)
    elif request.method == 'GET':
        if not request.session.has_key('username'):
            return render(request, 'core/login.html', {'form': form, 'login_error': None})
        return redirect(f'/profile/{request.session.get("username")}')


@csrf_exempt
def register(request: HttpRequest):
    form = RegisterForm()
    context = {
        'session': request.session,
        'form': form,
        'error': False
    }
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        return handlers.UserRequests.register_user(request, context, username, password)
    elif request.method == 'GET':
        if not request.session.has_key('username'):
            return render(request, 'core/register.html', {'form': form, 'login_error': None})
        return redirect(f'/profile/{request.session.get("username")}')


def profile(request: HttpRequest, username, tab=None):
    if request.method == 'GET':
        context = {
            'session': request.session
        }
        tab = request.GET.get('tab', None)
        if tab == 'profile':
            return handlers.UserRequests.user_profile(request, context, username)
        if tab == 'activity':
            return handlers.UserRequests.user_activity(request, context, username)
        if tab == 'edit':
            return handlers.UserRequests.user_edit(request, context, username)
        return handlers.UserRequests.user_profile(request, context, username)


def logout(request: HttpRequest):
    if request.method == 'GET' and 'username' in request.session:
        request.session.clear()
        return redirect('/')
    elif request.method != 'GET':
        return HttpResponse(status=405, content='Invalid method')
    else:
        return redirect('/')


def questions(request: HttpRequest):
    context = {
        'session': request.session
    }
    url_params = {
        'page': request.GET.get('page', 0),
        'order_by': QUESTION_FILTERS[request.GET.get('sort', 'Newest')],
        'answers_len' + ('__gte' if request.GET.get('filter', 'HasAnswers') != 'NoAnswers' else ''): 0
    }
    if request.method == 'GET':
        return handlers.QuestionRequests.get_recent_questions(request, context, url_params)


@csrf_exempt
def question(request: HttpRequest, question_id):
    context = {
        'session': request.session,
        'form': AnswerForm()
    }
    if request.method == 'GET':
        return handlers.QuestionRequests.get_question(request, context, question_id)
    elif request.method == 'POST':
        text = request.POST['body']
        user_id = request.session.get('id')
        return handlers.AnswerRequests.create_answer(request, context, text, question_id, user_id)


@csrf_exempt
def ask_question(request: HttpRequest):
    context = {
        'session': request.session,
        'form': QuestionForm()
    }
    if request.method == 'GET':
        if request.session.has_key('id'):
            return render(request, 'core/ask_question.html', context=context)
        return redirect('/login')
    elif request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.get('tags').strip().split(' ')
        user_id = request.session.get('id')
        return handlers.QuestionRequests.ask_question(request, title, body, tags, user_id, context)

