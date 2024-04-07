from django.urls import path
from . import views

app_name = 'parser'

urlpatterns = [
    path('start/', views.parser_interface_view, name='start'),
    path('report/', views.parser_intrepret_query, name='report'),
]