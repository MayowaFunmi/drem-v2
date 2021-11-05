from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('testimony/', views.testimony, name='testimony'),
    path('prayer_request/', views.prayer_request, name='prayer_request'),
    path('user_profile/<int:id>/', views.user_profile, name='user_profile'),
    path('update_user/', views.update_user, name='update_user'),
    path('about_us/', views.about_us, name='about_us'),
    path('about_the_convener/', views.convener, name='convener'),
    path('home/', views.base, name='home'),
    path('change_password/', views.change_password, name='change_password'),
    #path('password_reset/', views.password_reset, name='password_reset'),
]