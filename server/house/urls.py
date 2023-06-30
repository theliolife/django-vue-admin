from django.urls import path

from house.models import House
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard),
    path('list', views.list),
]