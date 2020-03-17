from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #login/out
    path("login", views.login_form, name="login_form"),
    path("login_view", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    #edit entries
    path('batch', views.batch, name='batch'),
    path('massupdate/<int:year>/<int:month>', views.massupdate, name='massupdate'),
    path('update/<int:year>/<int:month>', views.update, name='update'),
    path('unknown/<int:year>/<int:month>', views.unknown, name='unknown'),
    path('post_massupdate', views.post_massupdate, name='post_massupdate'),
    path('post_update', views.post_update, name='post_update'),
    ]
    