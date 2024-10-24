
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site, name='home'),  # Ensure 'home' is defined
    path('register/', views.register, name='register'),
    path('activation_sent/', views.activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),
    path('profile/', views.profile_update, name='profile_update'),
]