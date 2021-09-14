from django.urls import path

from api.views_templates.user import user as user_views
from api.views_templates.question import question as question_view
from api.views_templates.answer import answer as answer_view
from api.views_templates.tag import tag as tag_view


# http://localhost:8000/api/ + 

urlpatterns = [
    path('question/create', question_view.create_question),
    path('questions/', question_view.questions),
    path('question/<int:question_id>', question_view.question),
    path('question/<int:question_id>/votes', question_view.question_votes),
    path('question/<int:question_id>/views', question_view.question_views),
    path('question/<int:question_id>/text',  question_view.question_text),
    path('question/<int:question_id>/tags',  question_view.question_tags),
    path('question/<int:question_id>/answers', question_view.question_answers),
    path('question/<int:question_id>/user', question_view.question_user),

    path('user/create', user_views.create_user),
    path('users/', user_views.users),
    path('user/<str:username>', user_views.user),
    path('user/<str:username>/username', user_views.user_username),
    path('user/<str:username>/password', user_views.user_password),
    path('user/<str:username>/questions', user_views.user_questions),
    path('user/<str:username>/answers', user_views.user_answers),
    path('user/<str:username>/profile', user_views.user_profile),

    path('answer/create', answer_view.create_answer),
    path('answer/<int:answer_id>', answer_view.answer),
    path('answer/<int:answer_id>/text', answer_view.answer_text),
    path('answer/<int:answer_id>/likes', answer_view.answer_likes),
    path('answer/<int:answer_id>/question', answer_view.answer_question),
    path('answer/<int:answer_id>/user', answer_view.answer_user),

    path('tag/create', tag_view.create_tag),
    path('tags/<int:page_id>', tag_view.create_tag),
    path('tag/<str:tag_name>', tag_view.tag),
    path('tag/<str:tag_name>/count', tag_view.tag_count),
    path('tag/<str:tag_name>/questions', tag_view.tag_questions),
]
