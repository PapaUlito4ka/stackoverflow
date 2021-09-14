from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.authenticate import check_token, positive_response, negative_response
from core.models import Question
from api.handle_response import QuestionJson
import api.views_templates.question.question_handlers as question_handlers


FORMAT = 'json'
WRONG_TOKEN = 'Wrong token passed'
ERROR_STATUS = 403
OK_STATUS = 200

@csrf_exempt
@require_http_methods(['POST'])
def create_question(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Wrong token passed'))
    return question_handlers.question_create(request)

@csrf_exempt
@require_http_methods(['GET'])
def questions(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    return question_handlers.questions_get(request)

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def question(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return question_handlers.question_get(request, question_id)
    if request.method == 'PUT':
        return question_handlers.question_put(request, question_id)
    if request.method == 'DELETE':
        return question_handlers.question_delete(request, question_id)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def question_votes(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return question_handlers.question_votes_get(request, question_id)
    if request.method == 'PUT':
        return question_handlers.question_votes_put(request, question_id)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def question_views(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return question_handlers.question_views_get(request, question_id)
    if request.method == 'PUT':
        return question_handlers.question_views_put(request, question_id)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def question_text(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        question_handlers.question_text_get(request, question_id)
    if request.method == 'PUT':
        question_handlers.question_text_put(request, question_id)

@csrf_exempt
@require_http_methods(['GET'])
def question_tags(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        question_handlers.question_tags_get(request, question_id)

@csrf_exempt
@require_http_methods(['GET'])
def question_answers(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        question_handlers.question_answers_get(request, question_id)

@csrf_exempt
@require_http_methods(['GET'])
def question_user(request: HttpRequest, question_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        question_handlers.question_user_get(request, question_id)