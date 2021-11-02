from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('application_form/', views.application_form, name='application_form'),
    path('save_application_form/', views.application_form_save, name='save_application_form'),
    path('sbi_home/', views.bible_school_home, name='sbi_home'),
    path('code_login/', views.code_login, name='code_login'),
    path('instructions/', views.instructions, name='instructions'),
    path('apply/', views.apply_form, name='apply'),
]