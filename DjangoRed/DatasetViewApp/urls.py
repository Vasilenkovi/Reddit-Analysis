from django.urls import path
from . import views

app_name = 'dataset_view'

urlpatterns = [
    path('list/', views.datasets_list_view, name='list'),
    path('details/', views.datasets_view, name='details'),
    path('details/<int:page>', views.datasets_view, name='details_page'),
    path('download/', views.download_csv, name='download'),
]