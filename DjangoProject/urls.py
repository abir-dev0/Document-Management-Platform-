from django.contrib import admin
from django.urls import path, include

# Ces deux imports sont obligatoires pour MEDIA
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import CustomLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('myapp.urls')),  
]

#Ajoute ceci pour que Django serve les fichiers uploadés
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
