from django.urls import path
from . import views
app_name = 'awards'

urlpatterns = [
    path('create_award/', views.award_view, name='create_award'),
    path('list_awards/', views.award_list, name='list_awards'),
    path('delete_award/<int:id>/', views.delete_award, name='delete_award'),

]