from django.urls import path
from . import views

app_name = 'GraphApp'

urlpatterns = [
    path('base_graph/', views.base_graph_view, name='base_graph')
]