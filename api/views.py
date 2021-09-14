from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.core.serializers import serialize
from .authenticate import check_token, positive_response, negative_response
from core.models import User, Question, Answer
import json


FORMAT = 'json'
WRONG_TOKEN = 'Wrong token passed'

