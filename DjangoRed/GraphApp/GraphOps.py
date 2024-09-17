import networkx as nx

def calculate_jaccard_edges(sub_users_iter: tuple[object, tuple]) -> tuple[list, dict[tuple, float], float]:
    max_jaccard = 0
    edge_list = []
    edge_labels_dict = {}

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

    return edge_list, edge_labels_dict, max_jaccard

def get_centrality(graph: nx.Graph) -> list[tuple[object, float]]:
    centrality_dict = nx.eigenvector_centrality_numpy(graph, weight = "weight")
    centrality_list_sorted = list(map( 
        lambda x: (x[0], round(x[1], 5)), 
        centrality_dict.items())
    )
    centrality_list_sorted.sort(key = lambda x: x[1], reverse = True)

    return centrality_list_sorted

def get_communities(graph: nx.Graph) -> list[list[object]]:
    community_list = nx.community.greedy_modularity_communities(
            graph, 
            cutoff = 2,
            best_n = max(len(graph.nodes) // 2, 2), # Max ensures best_n >= cutoff
            weight = "weight"
        )
    community_list = [list(x) for x in community_list]

    return community_list