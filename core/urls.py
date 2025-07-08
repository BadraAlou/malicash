# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("process-mobile-transfer/", views.process_mobile_transfer, name="process_mobile_transfer"),
    #path('transfert/mobile/', views.effectuer_transfers_mobile, name='effectuer_transfer_mobile'),
    path("transfer-money/", views.process_mobile_transfer, name="transfer_money"),
    path("approve-transfer/<str:reference>/", views.approve_transfer, name="approve_transfer"),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('track/', views.track_transfer, name='track_transfer'),
    path('calculator/', views.calculator, name='calculator'),
    #path('agents/', views.find_agents, name='find_agents'),
    path('history/', views.transfer_history, name='transfer_history'),
    path('profile/', views.profile, name='profile'),
    path('support/', views.support, name='support'),
    path('referral/', views.referral, name='referral'),
    path('notifications/', views.notifications, name='notifications'),
    #path('nos-agents/', views.local_agents, name='local_agents'),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('about/', views.about, name='about'),
#     path('services/', views.services, name='services'),
#     path('faq/', views.faq, name='faq'),
#     path('contact/', views.contact, name='contact'),
#     path('terms/', views.terms, name='terms'),
#     path('privacy/', views.privacy, name='privacy'),
# ]