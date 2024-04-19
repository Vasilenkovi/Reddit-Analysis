from django.urls import path
from . import views

app_name = 'dataset_view'

urlpatterns = [
    path('list/', views.datasets_view, name='list'),
    #path('details/<dataset_id:slug>', views.parser_intrepret_query, name='report'),
]