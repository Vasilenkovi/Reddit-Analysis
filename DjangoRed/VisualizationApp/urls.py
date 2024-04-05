from . import views
from django.urls import path

app_name = "VisualizationApp"
urlpatterns = [
    path('visualization-app', views.visualization_app_view, name='visualization-app')
]