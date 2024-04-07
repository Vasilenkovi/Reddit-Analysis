from . import views
from django.urls import path

app_name = "HomeApp"
urlpatterns = [
    path('', views.home_view, name='home'),
    path('test_id', views.id_test, name='home_id')
]