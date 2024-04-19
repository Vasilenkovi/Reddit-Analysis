from django.shortcuts import render
from django.views.decorators.http import require_POST
from DjangoRed.settings import NATIVE_SQL_DATABASES
from IdApp.db_query import get_comment_datasets, get_user_datasets

# Create your views here.
def datasets_view(request):
    

    return render(request, "datasets/list.html", {
        "comment_sets": get_comment_datasets(),
        "user_sets": get_user_datasets(),
        "favorite_sets": []
    })