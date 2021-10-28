from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest
from django.db.models import Prefetch, F, Count
from django.forms.models import model_to_dict
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import Q

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
    try:
        if url_params.page:
            paginator = Paginator(questions, QUESTIONS_PER_PAGE)
            questions = paginator.page(url_params.page)
    except Exception as e:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(e.__str__()))
    serialized_question = dict()
    serialized_question['questions'] = [model_to_dict(question) for question in questions]
    for i, q in enumerate(questions):
        serialized_question['questions'][i]['tags'] = [model_to_dict(tag) for tag in q.tags.all()]
        serialized_question['questions'][i]['user'] = q.user.username
        serialized_question['questions'][i]['answers'] = len(q.answers)
    serialized_question['nav_info'] = {
        'cur_page': int(url_params.page),
        'all_pages': len(questions) // QUESTIONS_PER_PAGE + (not len(questions) % QUESTIONS_PER_PAGE == 0)
    }
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_question))


def questions_search(request: HttpRequest):
    p1 = Prefetch('tags')
    p2 = Prefetch('user')
    p3 = Prefetch('answer_set', to_attr='answers')

    query = request.GET.get('q', '')
    tags = request.GET.get('tags', '')
    user = request.GET.get('user', '')
    sort = request.GET.get('sort', '')
    filter_ = request.GET.get('filter', '')

    query_words = query.split(' ') if query else []
    query_tags = tags.split(' ') if tags else []
    query_user = user

    big_query = Q()
    if len(query_words) > 0:
        for i in range(len(query_words)):
            big_query |= Q(text__icontains=query_words[i]) | Q(title__icontains=query_words[i])
    if len(query_tags) > 0:
        for i in range(len(query_tags)):
            big_query |= Q(tags__name=query_tags[i])
    if len(query_user) > 0:
        big_query |= Q(user__username=query_user)
    if sort:
        if sort == 'Newest':
            sort = '-created_at'
        elif sort == 'MostVotes':
            sort = '-votes'
        elif sort == 'MostFrequent':
            sort = '-views'
        else:
            sort = '-created_at'
    if filter_:
        if filter_ == 'HasAnswers':
            big_query |= Q(answer__isnull=False)
        elif filter_ == 'NoAnswers':
            big_query |= Q(answer__isnull=True)
        else:
            big_query |= Q(answer__isnull=False)


    filtered_questions = Question.objects.prefetch_related(p1, p2, p3)\
        .filter(big_query)

    if sort:
        filtered_questions = filtered_questions.order_by(sort)

    serialized_questions = dict()
    serialized_questions['questions'] = [model_to_dict(question) for question in filtered_questions]
    for i, question in enumerate(filtered_questions):
        serialized_questions['questions'][i]['tags'] = [model_to_dict(tag) for tag in question.tags.all()]
        serialized_questions['questions'][i]['user'] = question.user.username
        serialized_questions['questions'][i]['answers'] = len(question.answers)

    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_questions))


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
        d['user'] = model_to_dict(User.objects.get(pk=int(d['user'])))
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
        p1 = Prefetch('user')
        question = Question.objects.prefetch_related(p1).get(pk=question_id)
        user = question.user
        if question.votes < Json.votes:
            user.reputation += 1
        else:
            user.reputation -= 1
        question.votes = Json.votes
        user.save()
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



