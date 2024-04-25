from django.shortcuts import render
import networkx as nx
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins
from DatasetViewApp.db_queries import sub_select_user_dataset_from_ids
from DatasetViewApp.forms import Dataset_operation_form

# Create your views here.
def base_graph_view(request):  
    context = {
        "dataset_ids": [],
        "data": [],
        "error": None,
        "downloadable": None
    }

    if request.method == "GET":
        return render()

    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()

    if not dataset_ids:
        return render(request, "", context = context)

    if not form.is_valid():
        context["error"] = "Unsupported dataset combination"
        context["dataset_ids"] = dataset_ids

        return render(request, "", context = context)

    column_list = ["su.user_full_name", "s.display_name"]
    user_data = sub_select_user_dataset_from_ids(column_list, dataset_ids)


    G = nx.complete_bipartite_graph(3, 3)
    fig, ax = plt.subplots(1, 1)
    nx.draw_networkx(G, ax=ax)
    html_embed_string = fig_to_html(fig)
    

    return render(request, "graphs/base_graph.html", {"html_embed": html_embed_string})