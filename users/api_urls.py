from django.urls import path
from .views import RegisterUserView, ProfileView
from . import api_views

urlpatterns = [
    # 🔐 Inscription via API (DRF generics)
    path('register/', RegisterUserView.as_view(), name='api_register'),

    # 👤 Profil utilisateur (récupération ou mise à jour)
    path('profile/<int:pk>/', ProfileView.as_view(), name='api_profile'),

    # 🔐 Inscription personnalisée (via fonction — exemple : Flutter)
    path('custom-register/', api_views.register_user, name='custom_register'),

    # 🔑 Connexion personnalisée (Flutter ou autre front)
    path('login/', api_views.LoginAPIView.as_view(), name='custom_login'),

    # 💸 Historique ou liste de transferts côté mobile
    path('transfers/', api_views.TransferAPIView.as_view(), name='api_transfers'),
]


# from django.urls import path
# from .views import RegisterUserView, ProfileView
# from . import api_views

# urlpatterns = [
#     path('register/', RegisterUserView.as_view(), name='register'),
#     path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
#     path('api/users/register/', api_views.register_user, name='api_register'),
#     path('users/login/', api_views.LoginAPIView.as_view(), name='api_login'),
#     path('transfers/', api_views.TransferAPIView.as_view(), name='api_transfers'),
# ]

