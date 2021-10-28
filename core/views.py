from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, EditProfileForm
from django.contrib import messages
from uuid import uuid4


import core.handlers.responses as handlers
from core.handlers.handlers import handle_uploaded_file
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
        'page': request.GET.get('page', 1),
        'order_by': QUESTION_FILTERS[request.GET.get('sort', 'Newest')],

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

@csrf_exempt
def profile(request: HttpRequest, username, tab=None):
    context = {
        'session': request.session
    }
    tab = request.GET.get('tab', None)
    if request.method == 'GET':
        if tab == 'profile':
            return handlers.UserRequests.user_profile(request, context, username)
        if tab in ('activity', 'summary'):
            return handlers.UserRequests.user_profile_activity(request, context, username)
        if tab == 'edit':
            context['form'] = EditProfileForm()
            return handlers.UserRequests.user_profile_edit(request, context, username)
        if tab == 'answers':
            return handlers.UserRequests.user_profile_answers(request, context, username)
        if tab == 'questions':
            return handlers.UserRequests.user_profile_questions(request, context, username)
        if tab == 'tags':
            return handlers.UserRequests.user_profile_tags(request, context, username)
        return handlers.UserRequests.user_profile(request, context, username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        context['filename'] = ''
        if 'img_file' in request.FILES:
            context['filename'] = request.FILES['img_file'].name
            idx = context['filename'].rindex('.')
            context['filename'] = context['filename'][:idx] + f'_{uuid4()}' + context['filename'][idx:]
            handle_uploaded_file(request.FILES['img_file'], context['filename'])
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
        'page': request.GET.get('page', 1),
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


def users(request: HttpRequest):
    context = {
        'session': request.session
    }
    url_params = {
        'page': request.GET.get('page', '1'),
        'username': request.GET.get('username', '')
    }

    if request.method == 'GET':
        return handlers.UserRequests.get_users(request, context, url_params)

@csrf_exempt
def search(request: HttpRequest):
    context = {
        'session': request.session
    }

    if request.method == 'GET':
        url_params = {
            'q': request.GET.get('q', ''),
            'tags': request.GET.get('tags', ''),
            'user': request.GET.get('user', ''),
            'sort': request.GET.get('sort', ''),
            'filter': request.GET.get('filter', '')
        }
        return handlers.QuestionRequests.search_question(request, context, url_params)
    if request.method == 'POST':
        url_params = {
            'q': request.POST.get('q', ''),
            'tags': request.POST.get('tags', ''),
            'user': request.POST.get('user', ''),
            'sort': request.GET.get('sort', ''),
            'filter': request.GET.get('filter', '')
        }

        return handlers.QuestionRequests.search_question(request, context, url_params)

def tags(request: HttpRequest):
    context = {
        'session': request.session
    }
    url_params = {
        'page': request.GET.get('page', '1'),
        'tag_name': request.GET.get('tag_name', '')
    }

    if request.method == 'GET':
        return handlers.TagRequests.get_tags(request, context, url_params)


