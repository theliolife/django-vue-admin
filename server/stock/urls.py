from django.urls import path

from . import views

urlpatterns = [
    path('json/', views.jsons),
    path('get_db/', views.getBasic),
    path('', views.index, name='index'),
]