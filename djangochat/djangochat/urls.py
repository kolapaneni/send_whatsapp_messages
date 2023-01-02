from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('message/', include('bot.urls')),
    path('room/', include('room.urls')),
    path('admin/', admin.site.urls),
]
