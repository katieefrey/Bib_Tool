from django.urls import path

from . import views

urlpatterns = [
    path('', views.bsindex, name='bsindex'),
    path('results', views.results, name='results'),
]