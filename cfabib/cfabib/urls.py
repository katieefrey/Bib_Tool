from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('bibtool.urls')),
    path('bibmanage/', include('bibmanage.urls')),
    path('admin/', admin.site.urls),
]