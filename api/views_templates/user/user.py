from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.serializers import serialize

from api.authenticate import check_token, positive_response, negative_response
from core.models import User, Question, Answer
from api.handle_response import UserJson, QuestionJson, TagJson, AnswerJson
import api.views_templates.user.user_handlers as user_handlers


FORMAT = 'json'
WRONG_TOKEN = 'Wrong token passed'
ERROR_STATUS = 403
OK_STATUS = 200
USERS_PER_PAGE = 36

@csrf_exempt
@require_http_methods(['POST'])
def create_user(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Wrong token passed'))
    return user_handlers.users_create(request)

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def user(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return user_handlers.user_get(request, username)
    if request.method == 'PUT':
        return user_handlers.user_put(request, username)
    if request.method == 'DELETE':
        return user_handlers.user_delete(request, username)

@csrf_exempt
@require_http_methods(['GET'])
def users(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return user_handlers.get_users(request, request.GET.get('page', '1'))

@csrf_exempt
@require_http_methods(['PUT'])
def user_username(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'PUT':
        return user_handlers.user_username_put(request, username)

@csrf_exempt
@require_http_methods(['PUT'])
def user_password(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'PUT':
        return user_handlers.user_password_put(request, username)

@csrf_exempt
@require_http_methods(['GET'])
def user_questions(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        user_handlers.user_questions_get(request, username)

@csrf_exempt
@require_http_methods(['GET'])
def user_answers(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        user_handlers.user_answers_get(request, username)

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def user_profile(request: HttpRequest, username):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return user_handlers.user_profile_get(request, username, request.GET.get('tab', 'profile'))
    if request.method == 'POST':
        return user_handlers.user_profile_post(request, username)
