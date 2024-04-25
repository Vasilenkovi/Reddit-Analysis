from django.shortcuts import render

# Create your views here.

def home_view(request):
    if request.session.get("test_ids"):
        return render(request, "home.html", context={'test_ids': request.session["test_ids"]})
    else:
        return render(request, "home.html", context={'test_ids': None})