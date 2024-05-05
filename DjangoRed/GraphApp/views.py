from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import fig_to_html
from DatasetViewApp.db_queries import sub_select_user_dataset_from_ids
from DatasetViewApp.forms import Dataset_operation_form
from IdApp.task_id_manager import Job_types

# Create your views here.
def base_graph_view(request):  
    context = {
        "dataset_ids": [],
        "error": None,
        "downloadable": None,
        "html_embed": None
    }
    
    if request.method == "GET":
        return render(request, "graphs/base_graph.html", context = context)
    
    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()
    
    if not dataset_ids:
        return render(request, "graphs/base_graph.html", context = context)
    
    context["dataset_ids"] = dataset_ids
    if not form.is_valid():
        context["error"] = "Unsupported dataset combination"
    
        return render(request, "graphs/base_graph.html", context = context)
    
    if form.get_common_job_id() != Job_types.PARSE_SUBREDDITS:
        context["error"] = "Only user datasets can be used for graph constuction"
    
        return render(request, "graphs/base_graph.html", context = context)
    
    column_list = ["su.user_full_name", "s.display_name"]
    user_data = sub_select_user_dataset_from_ids(column_list, dataset_ids)
    sub_users = {}
    edge_list = []
    edge_labels_dict = {}
    sub_set = set()
    max_jaccard = 0.0

    for user, sub in user_data:
        if not sub_users.get(sub):
            sub_users[sub] = set()
            
        sub_users[sub].add(user)
        sub_set.add(sub)

    # Iterate over all pairs of subreddits and calculate similarity
    sub_users_iter = tuple(sub_users.items())
    for i in range(len(sub_users_iter) - 1):
        i_sub, i_users = sub_users_iter[i]

        for j in range(i + 1, len(sub_users_iter)):
            j_sub, j_users = sub_users_iter[j]
            intersect = len(i_users.intersection(j_users))
            union = len(i_users.union(j_users))
            jaccard = round(intersect / union, 5)

            if jaccard > 0:
                max_jaccard = max(max_jaccard, jaccard)
                edge_list.append((i_sub, j_sub, jaccard))
                edge_labels_dict[(i_sub, j_sub)] = jaccard

            
    G = nx.Graph()
    G.add_nodes_from(sub_set)
    G.add_weighted_edges_from(edge_list)
    pos = nx.spring_layout(G)
    weights = tuple(map(lambda x: x[2], edge_list))

    fig, ax = plt.subplots(1, 1)
    nx.draw_networkx(
                        G, 
                        pos = pos,
                        ax = ax, 
                        edge_cmap = plt.cm.gnuplot2,
                        edge_vmin = 0.0, 
                        edge_vmax = max_jaccard*1.1, 
                        edge_color = weights
                    )
    nx.draw_networkx_edge_labels(G, pos = pos, edge_labels = edge_labels_dict)
    html_embed_string = fig_to_html(fig)
    context["html_embed"] = html_embed_string

    return render(request, "graphs/base_graph.html", context = context)