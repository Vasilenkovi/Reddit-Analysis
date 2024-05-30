from django.urls import path
from . import views

app_name = 'GraphApp'

urlpatterns = [
    path('base_graph/', views.base_graph_view, name='base_graph'),
    path('base_graph_download/', views.download_graph, name='base_graph_download'),
]