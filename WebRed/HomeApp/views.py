from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from IdApp.task_id_manager import Job_types, get_task_id

# Create your views here.

def home_view(request):
    if request.session.get("test_ids"):
        print(request.session["test_ids"])
        return render(request, "home.html", context={'test_ids': request.session["test_ids"]})
    else:
        return render(request, "home.html", context={'test_ids': None})

@require_POST
def id_test(request):

    request.session["test_ids"] = {
        'parse_com': get_task_id(Job_types.PARSE_COMMENTS, {'test_for_parse_comments': 'test value'}),
        'parse_sub': get_task_id(Job_types.PARSE_SUBREDDITS, {'test_for_parse_subs': 'test value'}),
        'cluster': get_task_id(Job_types.CLUSTER, {'test_for_clustering': 'test value'})
    }

    return redirect("/")