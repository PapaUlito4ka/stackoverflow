from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from django.db import IntegrityError
from api.handle_response import UserJson, QuestionJson, AnswerJson, TagJson
from core.models import User, Question, Tag, Answer
from api.authenticate import positive_response, negative_response

import json


FORMAT = 'json'
ERROR_STATUS = 403
OK_STATUS = 200

# USERS

def get_users(request: HttpRequest, page: str):
    users_per_page = 36
    users = list(User.objects.all())
    paginator = Paginator(users, users_per_page)
    try:
        users_page = paginator.page(page)
    except Exception as e:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(e.__str__()))
    users_serialized = dict()
    users_serialized['users'] = [model_to_dict(user, exclude=['password']) for user in users_page]
    users_serialized['nav_info'] = {
        'cur_page': int(page),
        'all_pages': len(users) // users_per_page + 1
    }
    return HttpResponse(status=OK_STATUS, content=positive_response(users_serialized))

###########

# USER

def users_create(request: HttpRequest):
    Json = UserJson(request.body)
    try:
        user = User.objects.create(
            username=Json.username,
            password=Json.password
        )
    except IntegrityError:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User already exist'))
    user_serialized = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(user_serialized))

def user_get(request: HttpRequest, username):
    try:
        p1 = Prefetch('question_set', to_attr='questions')
        p2 = Prefetch('answer_set', to_attr='answers')
        user = User.objects.prefetch_related(p1, p2).get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    serialized_user = model_to_dict(user)
    serialized_user['questions'] = [model_to_dict(question) for question in user.questions]
    serialized_user['answers'] = [model_to_dict(answer) for answer in user.answers]
    for i, question in enumerate(user.questions):
        serialized_user['questions'][i]['tags'] = []
        for tag in question.tags.all():
            serialized_user['questions'][i]['tags'].append(model_to_dict(tag))
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_user))

def user_put(request: HttpRequest, username):
    Json = UserJson(request.body)
    try:
        user = User.objects.get(username=username)
        user.update(
            username=Json.username,
            password=Json.password,
            img_path=Json.img_path,
            location=Json.location,
            title=Json.title,
            about=Json.about
        )
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Username is already occupied'))
    serialized_usr = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_usr))

def user_delete(request: HttpRequest, username):
    try:
        user = User.objects.get(username=username).delete()
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    serialized_d = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_d))

##########

# USERNAME

def user_username_get(request: HttpRequest, username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Username is already occupied'))
    data = json.dumps({ 'username': user.username })
    return HttpResponse(status=OK_STATUS, content=positive_response(data))

def user_username_put(request: HttpRequest, username):
    Json = UserJson(request.body)
    try:
        user = User.objects.get(username=username)
        user.update(username=Json.username)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('Username is already occupied'))
    serialized_usr = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_usr))

##########

# PASSWORD

def user_password_put(request: HttpRequest, username):
    Json = UserJson(request.body)
    try:
        user = User.objects.get(username=username)
        user.update(password=Json.password)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception as e:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(e.__str__()))
    serialized_usr = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_usr))

###########

# QUESTIONS

def user_questions_get(request: HttpRequest, username):
    try:
        p1 = Prefetch('question_set', to_attr='questions')
        user = User.prefetch_related(p1).objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))
    serialized_questions = model_to_dict(user.questions)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_questions))

###########

# ANSWERS

def user_answers_get(request, username):
    try:
        p1 = Prefetch('answer_set', to_attr='answers')
        user = User.prefetch_related(p1).objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(status=ERROR_STATUS, content=negative_response('User wasn\'t found'))
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))
    serialized_answers = model_to_dict(user.answers)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_answers))

###########

# PROFILE

def user_profile_get(request: HttpRequest, username: str, tab: str):
    try:
        serialized_data = {}
        if tab in ('profile', 'summary', 'activity'):
            user = User.objects.get(username=username)
            questions = Question.objects \
                .filter(user_id=user.pk)\
                .order_by('-votes')
            answers = Answer.objects\
                .filter(user_id=user.pk)\
                .order_by('-likes')
            questions_ids = Question.objects\
                .filter(user_id=user.pk)\
                .values_list('tags')\
                .distinct()
            tags = Tag.objects.filter(pk__in=questions_ids)
            serialized_data['user'] = model_to_dict(user)
            serialized_data['questions'] = []
            for question in questions:
                q_d = model_to_dict(question)
                q_d.pop('tags')
                serialized_data['questions'].append(q_d)
            serialized_data['answers'] = [model_to_dict(answer) for answer in answers]
            serialized_data['tags'] = [model_to_dict(tag) for tag in tags]
        elif tab == 'answers':
            user = User.objects.get(username=username)
            answers = Answer.objects\
                .filter(user_id=user.pk)\
                .order_by('-likes')
            serialized_data['user'] = model_to_dict(user)
            serialized_data['answers'] = [model_to_dict(answer) for answer in answers]
        elif tab == 'questions':
            p1 = Prefetch('tags')
            user = User.objects.get(username=username)
            questions = Question.objects.prefetch_related(p1)\
                .filter(user_id=user.pk)\
                .order_by('-votes')
            serialized_data['user'] = model_to_dict(user)
            serialized_data['questions'] = []
            for question in questions:
                q_d = model_to_dict(question)
                q_d['tags'] = []
                for tag in question.tags.all():
                    q_d['tags'].append(model_to_dict(tag))
                serialized_data['questions'].append(q_d)
        elif tab == 'tags':
            user = User.objects.get(username=username)
            questions_ids = Question.objects \
                .filter(user_id=user.pk) \
                .values_list('tags') \
                .distinct()
            tags = Tag.objects.filter(pk__in=questions_ids)
            serialized_data['user'] = model_to_dict(user)
            serialized_data['tags'] = [model_to_dict(tag) for tag in tags]
        elif tab == 'edit':
            user = User.objects.get(username=username)
            serialized_data['user'] = model_to_dict(user)
        else:
            raise Exception(f'Tab "{tab}" does not exist')
        return HttpResponse(status=OK_STATUS, content=positive_response(serialized_data))
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))


def user_profile_post(request: HttpRequest, username: str):
    Json = UserJson(request.body)
    try:
        user = User.objects.get(username=username)
        filtered_users = User.objects.filter(username=Json.username)
        if len(filtered_users) == 0 or filtered_users[0].username == user.username:
            user.username = Json.username
        else:
            raise Exception('User with given username already exists.')
        user.about = Json.about
        if Json.img_path != '':
            user.img_path = Json.img_path
        user.save()
    except Exception as err:
        return HttpResponse(status=ERROR_STATUS, content=negative_response(err.__str__()))

    serialized_data = model_to_dict(user)
    return HttpResponse(status=OK_STATUS, content=positive_response(serialized_data))
