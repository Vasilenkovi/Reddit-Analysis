def calculate_jaccard_edges(sub_users_iter):
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