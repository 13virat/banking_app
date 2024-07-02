from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_account/', views.create_account, name='create_account'),
    path('accounts/', views.account_list, name='account_list'),
    path('account/<int:account_id>/', views.account_detail, name='account_detail'),
]
