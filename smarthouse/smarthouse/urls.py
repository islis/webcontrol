from django.contrib import admin
from django.urls import path, include
from .views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', index, name='main'),
                  path('user/', include('user.urls', 'user')),
                  path('device/', include('device.urls')),
                  path('rooms/', include('groups.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
