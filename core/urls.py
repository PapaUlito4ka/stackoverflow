from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login', views.login, name='login'),
    re_path(r'^profile/(?P<username>\w{0,50})(?P<tab>\w{0,20})?$', views.profile, name='profile'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('questions', views.questions, name='questions'),
    path('question/<int:question_id>', views.question, name='question'),
    path('questions/ask', views.ask_question, name='ask_question'),
    path('users', views.users, name='users')
]
