from django.urls import path

from . import views

urlpatterns = [
    path('', views.bmindex, name='bmindex'),
    path('add', views.add, name='add'),
    path('batch', views.batch, name='batch'),
    path('batch/<int:batchid>', views.viewbatch, name='viewbatch'),
    path('export', views.export, name='export'),
    path('add_post', views.add_post, name='add_post'),
    path('delete_post', views.delete_post, name='delete_post'),
    path('select_criteria', views.select_criteria, name='select_criteria'),
    #path('results', views.results, name='results'),
    #submit to ads
    path('submitads', views.submitads, name='submitads'),
]