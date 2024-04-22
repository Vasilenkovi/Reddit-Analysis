from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.http import HttpResponse
from IdApp.db_query import get_comment_datasets, get_user_datasets, execute
from IdApp.task_id_manager import Job_types
from .forms import Dataset_operation_form
from .db_queries import select_comment_dataset_from_ids, select_user_dataset_from_ids
from io import StringIO
import csv
from DjangoRed.settings import NATIVE_SQL_DATABASES
from json import dumps

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
        "headers": [],
        "error": None,
        "downloadable": None
    }

    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()

    if not form.is_valid():
        context["error"] = "Unsupported dataset combination"
        context["dataset_ids"] = dataset_ids

        return render(request, "datasets/details.html", context = context)
    
    dataset_type = form.fields["common_job"]
    headers = []
    data = []
    downloadable = False

    match dataset_type:
        case Job_types.PARSE_COMMENTS:
            data, headers = select_comment_dataset_from_ids(dataset_ids)
            downloadable = True

        case Job_types.PARSE_SUBREDDITS:
            data, headers = select_user_dataset_from_ids(dataset_ids)
            downloadable = True

        case _:
            context["error"] = "Unsupported dataset id"
            context["dataset_ids"] = dataset_ids

            return render(request, "datasets/details.html", context = context)

    context["dataset_ids"] = dataset_ids
    context["data"] = data
    context["headers"] = headers
    context["downloadable"] = downloadable

    return render(request, "datasets/details.html", context = context)

@require_POST
def download_csv(request):
    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()

    if not form.is_valid():
        return redirect("DatasetViewApp:details")
    
    dataset_type = form.fields["common_job"]
    headers = []
    data = []

    match dataset_type:
        case Job_types.PARSE_COMMENTS:
            data, headers = select_comment_dataset_from_ids(dataset_ids)

        case Job_types.PARSE_SUBREDDITS:
            data, headers = select_user_dataset_from_ids(dataset_ids)

    with StringIO(newline='') as f:
        csv.writer(f).writerow(headers)
        csv.writer(f).writerows(data)

        clean_ids = list(map(lambda x: x[5:], dataset_ids)) # strip away common prefix and underscore
        file_name = dataset_type + "_({ids})".format(ids = "_".join(clean_ids)) + ".csv"

        file_to_send = ContentFile(f.getvalue(), file_name)
        response = HttpResponse(file_to_send)
        response["Content-Type"] = "text/csv"
        response["Content-Length"] = file_to_send.size
        response["Content-Disposition"] = "attachment; filename=" + '"{f_name}"'.format(f_name = file_name)

        return response

        