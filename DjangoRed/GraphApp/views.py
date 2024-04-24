from django.shortcuts import render
import networkx as nx
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins

# Create your views here.
def base_graph_view(request):
    G = nx.complete_bipartite_graph(3, 3)
    fig, ax = plt.subplots(1, 1)
    nx.draw_networkx(G, ax=ax)
    html_embed_string = fig_to_html(fig)

    return render(request, "graphs/base_graph.html", {"html_embed": html_embed_string})