from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('store/', include('store.urls')),
    path('gimnasio/', include('gimnasio.urls')),
    path('api/', include('gimnasio.api_urls')),
]