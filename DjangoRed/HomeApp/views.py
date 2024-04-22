from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from IdApp.task_id_manager import Job_types, get_task_id

# Create your views here.

def home_view(request):
    if request.session.get("test_ids"):
        return render(request, "home.html", context={'test_ids': request.session["test_ids"]})
    else:
        return render(request, "home.html", context={'test_ids': None})