from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.authenticate import check_token, positive_response, negative_response
import api.views_templates.tag.tag_handlers as tag_handlers


FORMAT = 'json'
WRONG_TOKEN = 'Wrong token passed'
ERROR_STATUS = 403
OK_STATUS = 200

@csrf_exempt
@require_http_methods(['POST'])
def create_tag(request: HttpRequest):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Wrong token passed'))
    return tag_handlers.tag_create(request)

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def tag(request: HttpRequest, tag_name):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        return tag_handlers.tag_get(request, tag_name)
    if request.method == 'PUT':
        return tag_handlers.tag_put(request, tag_name)
    if request.method == 'DELETE':
        return tag_handlers.tag_delete(request, tag_name)

@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def tag_count(request: HttpRequest, tag_name):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        tag_handlers.tag_count_get(request, tag_name)
    if request.method == 'PUT':
        tag_handlers.tag_count_put(request, tag_name)

@csrf_exempt
@require_http_methods(['GET'])
def tag_questions(request: HttpRequest, tag_name):
    if not check_token(request):
        return HttpResponse(status=ERROR_STATUS, content=negative_response(WRONG_TOKEN))
    if request.method == 'GET':
        tag_handlers.tag_questions_get(request, tag_name)