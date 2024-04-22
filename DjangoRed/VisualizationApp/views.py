from django.shortcuts import render
from .forms import VisualizationForm
from DatasetViewApp.forms import Dataset_operation_form
from IdApp.task_id_manager import Job_types 
# Create your views here.
def visualization_app_view(request):
    context = {} 
    visualization_form = VisualizationForm(request.POST or None)
    context['visualization_form']= visualization_form 
    if request.method == 'POST':
        dataset_form = Dataset_operation_form(request=request)
        dataset_ids = dataset_form.get_ids_as_list()
        if not dataset_form.is_valid():
            # TODO : error message
            return render(request, "index.html", context) 

        job_id = dataset_form.get_common_job_id();
        if (job_id != Job_types.PARSE_COMMENTS):
            # TODO : error message
            return render(request, "index.html", context) 
        
        context['dataset_ids'] = dataset_ids
        return render(request, "index.html", context)

    else:    
        return render(request, "index.html", context) 