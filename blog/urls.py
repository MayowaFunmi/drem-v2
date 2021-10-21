from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='post_new'),
    path('', views.post_list, name='post_list'),
    path('<int:id>/<str:slug>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('add_category/', views.add_category, name='add_category'),
    path("<category>/", views.blog_category, name="blog_category"),

]
