from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admins/', admin.site.urls),
    path('api/',include('userside.urls')),
    path('admin/',include('adminside.urls')),
    path('rentals/',include('rentals.urls')),
    path('chat/',include('chat.urls')),
    # path('chat/', include('chat.routing.websocket_urlpatterns')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
