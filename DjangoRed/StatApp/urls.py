from django.urls import path
from . import views

app_name = 'StatApp'

urlpatterns = [
    path('', views.stat_view, name='stat')
]