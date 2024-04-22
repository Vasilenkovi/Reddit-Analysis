from django.shortcuts import render
from django.views.decorators.http import require_POST
from IdApp.db_query import get_comment_datasets, get_user_datasets
from IdApp.task_id_manager import Job_types
from .forms import Dataset_operation_form
from .db_queries import select_comment_dataset_from_ids

# Create your views here.
def datasets_list_view(request):
    

    return render(request, "datasets/list.html", {
        "comment_sets": get_comment_datasets(),
        "user_sets": get_user_datasets(),
        "favorite_sets": []
    })

@require_POST
def datasets_view(request):
    context = {
        "dataset_ids": [],
        "data": [],
        "headers": []
    }

    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()

    if not form.is_valid():
        return render(request, "datasets/details.html", context = context)
    
    dataset_type = form.fields["common_job"]
    headers = []
    data = []

    match dataset_type:
        case Job_types.PARSE_COMMENTS:
            data, headers = select_comment_dataset_from_ids(dataset_ids)

        case Job_types.PARSE_SUBREDDITS:
            pass

        case _:
            pass

    context["dataset_ids"] = dataset_ids
    context["data"] = data
    context["headers"] = headers

    return render(request, "datasets/details.html", context = context)