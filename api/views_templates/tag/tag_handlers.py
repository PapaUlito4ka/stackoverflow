from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest
from django.core import exceptions
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch

from api.handle_response import TagJson
from core.models import Tag
from api.authenticate import positive_response, negative_response

import json


FORMAT = 'json'
ERROR_STATUS = 403
OK_STATUS = 200

# CREATE TAG

def tag_create(request: HttpRequest):
    Json = TagJson(request.body)
    try:
        tag = Tag.objects.create(
            name=Json.name,
            count=Json.count
        )
    except IntegrityError:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag already exists'))
    tag_serialized = model_to_dict(tag)
    return HttpResponse(status=OK_STATUS, content=positive_response(tag_serialized))

###############

# TAG

def tag_get(request: HttpRequest, tag_id):
    try:
        p1 = Prefetch('question_set', to_attr='questions')
        tag = Tag.objects.prefetch_related(p1).get(pk=tag_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    serialized_tag = model_to_dict(tag)
    serialized_tag['questions'] = [model_to_dict(question) for question in tag.questions]
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_tag))

def tag_put(request: HttpRequest, tag_id):
    Json = TagJson(request.body)
    try:
        tag = Tag.objects.get(pk=tag_id)
        tag.update(
            name=Json.name,
            count=Json.count
        )
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))
    serialized_tag = model_to_dict(tag)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_tag))

def tag_delete(request: HttpRequest, tag_id):
    try:
        tag = Tag.objects.get(pk=tag_id).delete()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    serialized_tag = model_to_dict(tag)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_tag))

###############

# TAG COUNT

def tag_count_get(request: HttpRequest, tag_id):
    try:
        tag = Tag.objects.get(pk=tag_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    count = json.dumps({ 'count': tag.count })
    return HttpResponse(status=OK_STATUS, content=positive_response(count))

def tag_count_put(request: HttpRequest, tag_id):
    Json = TagJson(request.body)
    try:
        tag = Tag.objects.get(pk=tag_id)
        tag.update(count=Json.count)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))
    count = json.dumps({ 'count': tag.count })
    return HttpResponse(status=OK_STATUS, content=positive_response(count))

###############

# TAG QUESTIONS

def tag_questions_get(request: HttpRequest, tag_id):
    try:
        p1 = Prefetch('question_set', to_attr='questions')
        tag = Tag.objects.prefetch_related(p1).get(pk=tag_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Tag wasn\'t found'))
    questions = json.dumps( { 'questions': [model_to_dict(question) for question in tag.questions] })
    return HttpResponse(status=OK_STATUS, content=positive_response(questions))

###############