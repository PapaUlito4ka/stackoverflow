from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import InterfaceError
from django.db.models import Prefetch, F

from api.handle_response import AnswerJson
from core.models import Answer
from api.authenticate import positive_response, negative_response

import json


FORMAT = 'json'
ERROR_STATUS = 403
OK_STATUS = 200

# CREATE ANSWER

def answer_create(request: HttpRequest):
    Json = AnswerJson(request.body)
    try:
        if len(Answer.objects.filter(user_id=Json.user, question_id=Json.question)) != 0:
            raise Exception('You have already posted answer to this question!')
        answer = Answer.objects.create(
            text=Json.text,
            question_id=Json.question,
            user_id=Json.user
        )
    except Exception as e:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(e.__str__()))
    serialized_answer = model_to_dict(answer)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answer))

###############

# ANSWER


def answer_get(request: HttpRequest, answer_id):
    try:
        p1 = Prefetch('user')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    serialized_answer = model_to_dict(answer)
    serialized_answer['user'] = model_to_dict(answer.user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answer))


def answer_put(request: HttpRequest, answer_id):
    Json = AnswerJson(request.body)
    try:
        p1 = Prefetch('user')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
        answer.text = Json.text
        answer.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    serialized_answer = model_to_dict(answer)
    serialized_answer['user'] = model_to_dict(answer.user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answer))


def answer_delete(request: HttpRequest, answer_id):
    try:
        p1 = Prefetch('user')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
        answer.delete()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    serialized_answer = model_to_dict(answer)
    serialized_answer['user'] = model_to_dict(answer.user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answer))

###############

# ANSWER TEXT


def answer_text_get(request: HttpRequest, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    data = json.dumps({ 'text': answer.text })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


def answer_text_put(request: HttpRequest, answer_id):
    Json = AnswerJson(request.body)
    try:
        answer = Answer.objects.get(pk=answer_id)
        answer.text = Json.text
        answer.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    data = json.dumps({ 'text': answer.text })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))

###############

# ANSWER LIKES


def answer_likes_get(request: HttpRequest, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    data = json.dumps({ 'likes': answer.likes })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


def answer_likes_put(request: HttpRequest, answer_id):
    Json = AnswerJson(request.body)
    try:
        p1 = Prefetch('user')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
        user = answer.user
        if answer.likes < Json.likes:
            user.reputation += 1
        else:
            user.reputation -= 1
        answer.likes = Json.likes
        user.save()
        answer.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    data = json.dumps({ 'likes': answer.likes })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))

###############

# ANSWER QUESTION


def answer_question_get(request: HttpRequest, answer_id):
    try:
        p1 = Prefetch('question')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, context=negative_response('Answer does not exist'))
    data = json.dumps({ 'question': answer.question })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))

###############

# ANSWER USER


def answer_user_get(request: HttpRequest, answer_id):
    try:
        p1 = Prefetch('user')
        answer = Answer.objects.prefetch_related(p1).get(pk=answer_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Answer does not exist'))
    data = json.dumps({ 'user': answer.user })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))

###############