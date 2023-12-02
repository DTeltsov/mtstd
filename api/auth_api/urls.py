from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountsByLoginView.as_view({'patch': 'partial_update'}), name='accounts'),
    path('login/', views.AuthView.as_view(), name='login'),
    path('login_by_token/', views.LoginByToken.as_view(), name='login_by_token'),
    path('creator/', views.AccountsView.as_view(), name='account_creator_create')
]
