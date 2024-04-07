from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import Http404
from .forms import Submission_parsing_form, Subreddit_parsing_form, Subreddit_users_parsing_form
from IdApp.task_id_manager import get_task_id, Job_types
from .tasks import parse_submissions, parse_subreddit, parse_users

# Create your views here.
def parser_interface_view(request):
    return render(request, "parser/interface.html", {
        "submission_parsing_form": Submission_parsing_form(),
        "subreddit_parsing_form": Subreddit_parsing_form(),
        "subreddit_users_parsing_form": Subreddit_users_parsing_form()
    })

@require_POST
def parser_intrepret_query(request):
    job_id = None
    form_type = request.POST['form_type']

    match form_type:
        case "comment_submission":
            form_data = Submission_parsing_form(request.POST)

            if form_data.is_valid():
                data = form_data.cleaned_data
                job_id = get_task_id(Job_types.PARSE_COMMENTS, data)
                parse_submissions.delay(job_id, data)

        case "comment_subreddit":
            form_data = Subreddit_parsing_form(request.POST)
            
            if form_data.is_valid():
                data = form_data.cleaned_data
                job_id = get_task_id(Job_types.PARSE_COMMENTS, data)
                parse_subreddit.delay(job_id, data)

        case "users":
            form_data = Subreddit_users_parsing_form(request.POST)
            
            if form_data.is_valid():
                data = form_data.cleaned_data
                job_id = get_task_id(Job_types.PARSE_SUBREDDITS, data)
                parse_users.delay(job_id, data)

        case _:
            raise Http404

    return render(request, "parser/report.html", {"job_id": job_id})