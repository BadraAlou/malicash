from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('transfers/', include('transfers.urls')),

    # API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/core/', include('core.api_urls')),
    path('api/users/', include('users.api_urls')),
    path('api/transfers/', include('transfers.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# # JWT Authentication
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# urlpatterns = [
#     # Admin
#     path('admin/', admin.site.urls),

#     # Web App URLs
#     path('', include('core.urls')),                       # Accueil et pages publiques
#     path('users/', include('users.urls')),                # Inscription, connexion (site)
#     path('transfers/', include('transfers.urls')),        # Transferts depuis le site

#     # Authentification API (pour Flutter ou autres)
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#     # API personnalisées (pour Flutter, React ou autres)
#     path('api/core/', include('core.api_urls')),
#     path('api/transfers/', include('transfers.api_urls')),
#     path('api/users/', include('users.api_urls')),
# ]

# # Gestion des fichiers media en mode debug
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
