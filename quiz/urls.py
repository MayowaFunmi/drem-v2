from django.urls import path
from . import views
app_name = 'quiz'

urlpatterns = [
    path('take_questions/', views.questions, name='take_questions'),
    path('take_questions/answers/', views.answers, name='answers'),
    path('welcome/', views.welcome, name='welcome'),
    path('check/', views.check, name='check'),
    #path('index/', views.index, name='index'),
    #path('save_ans/', views.save_ans, name='save_ans'),
    #path('result/', views.result, name='result'),
    path('add_quiz', views.add_question, name='add_quiz'),
    path('all_questions/', views.all_questions, name='all_questions'),
    path('delete_question/<int:id>/', views.delete_questions, name='delete_question'),
    path('ajax_quiz/', views.Quiz.as_view(), name='ajax_quiz')
]
