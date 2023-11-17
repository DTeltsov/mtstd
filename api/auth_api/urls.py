from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountsByLoginView.as_view({'patch': 'partial_update'}), name='accounts'),
    path('creator/', views.AccountsView.as_view(), name='account_creator_create')
]
