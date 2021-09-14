from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest
from django.db.models import Prefetch, F, Count
from django.forms.models import model_to_dict
from django.core import exceptions
from django.core.paginator import Paginator

from api.handle_response import UserJson, QuestionJson, AnswerJson, TagJson, UrlParamsDict
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from api.handle_response import QuestionJson
from core.models import Question, User
from api.authenticate import positive_response, negative_response, to_dict
import json

from core.models import Tag

FORMAT = 'json'
ERROR_STATUS = 403
OK_STATUS = 200
QUESTIONS_PER_PAGE = 36


# CREATE QUESTION

def question_create(request: HttpRequest):
    Json = QuestionJson(request.body)
    try:
        tags = []
        for tag_name in Json.tags:
            tag = Tag.objects.filter(name=tag_name)
            if len(tag) == 0:
                tags.append(Tag.objects.create(name=tag_name).pk)
            else:
                tags.append(tag[0])
        question = Question.objects.create(
            title=Json.title,
            text=Json.text,
            user_id=Json.user
        )
        question.tags.add(*tags)
    except Exception as e:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(e.__str__()))
    serialized_question = model_to_dict(question)
    serialized_question['tags'] = [model_to_dict(tag) for tag in question.tags.all()]
    serialized_question['answers'] = []
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


###########

# QUESTIONS

def questions_get(request: HttpRequest):
    url_params = UrlParamsDict(request.GET.dict())
    p1 = Prefetch('tags')
    p2 = Prefetch('user')
    p3 = Prefetch('answer_set', to_attr='answers')
    questions = Question.objects.prefetch_related(p1, p2, p3).all() \
        .annotate(answers_len=Count('answer'))
    questions = questions.filter(**url_params.filter_dict)
    if url_params.order_by:
        questions = questions.order_by(url_params.order_by)
    if url_params.page:
        paginator = Paginator(questions, QUESTIONS_PER_PAGE)
        serialized_question = [model_to_dict(question) for question in paginator.get_page(url_params.page).object_list]
    else:
        serialized_question = [model_to_dict(question) for question in questions]
    for i, question in enumerate(questions):
        q = Question.objects.prefetch_related(p1, p2, p3).get(pk=question.pk)
        serialized_question[i]['tags'] = [model_to_dict(tag) for tag in q.tags.all()]
        serialized_question[i]['user'] = q.user.username
        serialized_question[i]['answers'] = len(q.answers)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


###########

# QUESTION

def question_get(request: HttpRequest, question_id):
    try:
        p1 = Prefetch('tags')
        p2 = Prefetch('user')
        p3 = Prefetch('answer_set', to_attr='answers')
        question = Question.objects.prefetch_related(p1, p2, p3).get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_question = model_to_dict(question)
    serialized_question['tags'] = [model_to_dict(tag) for tag in question.tags.all()]
    serialized_question['user'] = model_to_dict(question.user)
    serialized_question['answers'] = []
    for answer in sorted(question.answers, key=lambda obj: obj.likes, reverse=True):
        d = model_to_dict(answer)
        d['user'] = User.objects.get(pk=int(d['user'])).username
        serialized_question['answers'].append(d)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


def question_put(request: HttpRequest, question_id):
    Json = QuestionJson(request.body)
    try:
        question = Question.objects.get(pk=question_id).update(
            text=Json.text
        )
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_question = model_to_dict(question)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


def question_delete(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question.delete()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_question = model_to_dict(question)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


###########

# QUESTION VOTES

def question_votes_get(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'votes': question.votes})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


def question_votes_put(request: HttpRequest, question_id):
    Json = QuestionJson(request.body)
    try:
        question = Question.objects.get(pk=question_id)
        question.votes = Json.votes
        question.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'votes': question.votes})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


############

# QUESTION VIEWS

def question_views_get(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'views': question.views})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


def question_views_put(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question.views += 1
        question.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'views': question.views})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


#############

# QUESTION TEXT

def question_text_get(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'text': question.text})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


def question_text_put(request: HttpRequest, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question.text = request.body['text']
        question.save()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    data = json.dumps({'text': question.text})
    return HttpResponse(status=OK_STATUS, content=positive_response(data))


##############

# QUESTION TAGS

def question_tags_get(request: HttpRequest, question_id):
    try:
        p1 = Prefetch('tag_set', to_attr='tags')
        question = Question.objects.prefetch_related(p1).get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_tags = model_to_dict(question.tags)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_tags))


##############

# QUESTION ANSWERS

def question_answers_get(request: HttpRequest, question_id):
    try:
        p1 = Prefetch('answer_set', to_attr='answers')
        question = Question.objects.prefetch_related(p1).get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_answers = model_to_dict(question.answers)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answers))


# QUESTION USER

def question_user_get(request: HttpRequest, question_id):
    try:
        p1 = Prefetch('user')
        question = Question.objects.prefetch_related(p1).get(pk=question_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
    serialized_user = model_to_dict(question.user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_user))

# def question_answers_post(request: HttpRequest, question_id):
#     try:
#         p1 = Prefetch('answer_set', to_attr='answers')
#         question = Question.prefetch_related(p1).objects.get(pk=question_id)
#         question.answers.create(
#             text=request.body['text'],
#             question=question,
#             user=request.body['user_id']
#         )
#     except ObjectDoesNotExist:
#         return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
#     except IntegrityError:
#         return HttpResponse(status=ERROR_STATUS, content=negative_response('Could not create answer'))
#     serialized_question = model_to_dict(question)
#     return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))

# def question_answers_put(request: HttpRequest, question_id):
#     try:
#         p1 = Prefetch('answer_set', to_attr='answers')
#         question = Question.prefetch_related(p1).objects.get(pk=question_id)
#         question.answers.update(
#             text=request.body['text']
#         )
#     except ObjectDoesNotExist:
#         return HttpResponse(status=ERROR_STATUS, content=negative_response('Question does not exist'))
#     except IntegrityError:
#         return HttpResponse(status=ERROR_STATUS, content=negative_response('Could not create answer'))
#     serialized_question = model_to_dict(question)
#     return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))

##############
