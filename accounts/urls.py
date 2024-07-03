from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/create/', views.create_account, name='create_account'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(success_url='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('download_statement/', views.download_statement, name='download_statement'),
]
