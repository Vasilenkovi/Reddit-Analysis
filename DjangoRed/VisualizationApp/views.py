from django.shortcuts import render
from .forms import VisualizationForm
# Create your views here.
def visualization_app_view(request):
    context = {} 
    form = VisualizationForm(request.POST or None)
    context['form']= form 
    if request.POST: 
        if form.is_valid(): 
            temp = form.cleaned_data.get("clasterization_method") 
            print(temp) 
    
    return render(request, "index.html", context) 