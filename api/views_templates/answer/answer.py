from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.authenticate import check_token, positive_response, negative_response
import api.views_templates.answer.answer_handlers as answer_handlers


FORMAT = 'json'
WRONG_TOKEN = 'Wrong token passed'
ERROR_STATUS = 403
OK_STATUS = 200

@csrf_exempt
@require_http_methods(['POST'])
def create_answer(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Wrong token passed'))
    return answer_handlers.answer_create(request)

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def answer(request: HttpRequest, answer_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return answer_handlers.answer_get(request, answer_id)
    if request.method == 'PUT':
        return answer_handlers.answer_put(request, answer_id)
    if request.method == 'DELETE':
        return answer_handlers.answer_delete(request, answer_id)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def answer_text(request: HttpRequest, answer_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        answer_handlers.answer_text_get(request, answer_id)
    if request.method == 'PUT':
        answer_handlers.answer_text_put(request, answer_id)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def answer_likes(request: HttpRequest, answer_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return answer_handlers.answer_likes_get(request, answer_id)
    if request.method == 'PUT':
        return answer_handlers.answer_likes_put(request, answer_id)

@csrf_exempt
@require_http_methods(['GET'])
def answer_question(request: HttpRequest, answer_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        answer_handlers.answer_question_get(request, answer_id)

@csrf_exempt
@require_http_methods(['GET'])
def answer_user(request: HttpRequest, answer_id):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        answer_handlers.answer_user_get(request, answer_id)
