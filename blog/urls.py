from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('new/', views.post_create, name='post_new'),
    path('', views.post_list, name='post_list'),
    path('<int:id>/<str:slug>/', views.post_detail, name='post_detail'),
    path('<int:id>/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('<int:id>/<str:slug>/delete/', views.post_delete, name='post_delete'),
    path('add_category/', views.add_category, name='add_category'),
    path("<category>/", views.blog_category, name="blog_category"),
    path('like/<int:id>/<str:slug>/', views.like_view, name='like_post'),
]
