from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.transfer_money, name='transfer_money'),
    path('history/', views.transfer_history, name='transfer_history'),
    path('agents/', views.agents_page, name='agents_page'),
    #path('detail/<str:reference>/', views.transfer_detail, name='transfer_detail'),
    path('transfers/detail/<str:reference>/', views.transfer_detail, name='transfer_detail'),
    path('track/', views.track_transfer, name='track_transfer'),
    path('calculator/', views.calculator, name='calculator'),
    #path('agents/', views.find_agents, name='find_agents'),
]