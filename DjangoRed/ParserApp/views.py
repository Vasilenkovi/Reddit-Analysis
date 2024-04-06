from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import Parse_form

# Create your views here.
def parser_interface_view(request):
    return render(request, "parser/interface.html", {"interface_form": Parse_form()})

@require_POST
def parser_intrepret_query(request):
    return render(request, "parser/report.html")