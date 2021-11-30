from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls')),
    path('', include('home.urls')),
    path('', include('contest.urls')),
]
