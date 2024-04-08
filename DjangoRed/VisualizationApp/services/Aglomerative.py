from sklearn.cluster import AgglomerativeClustering
import numpy as np
class AgloDivMethod:
    def __init__(self,doc_to_doc_matrix):
        self.doc_to_doc_matrix = doc_to_doc_matrix
        result = None
    def cluster(self, divisionary, metric, cluster_count):
        X = self.doc_to_doc_matrix
        if(divisionary=="Div"):
            metric = "euclidean"
            clustering = AgglomerativeClustering(metric=metric, linkage='complete', n_clusters=cluster_count).fit(X)
        else:
            metric = "euclidean"
            clustering = AgglomerativeClustering(metric=metric, n_clusters=cluster_count).fit(X)
        self.save_to_db()
        self.result = clustering.labels_
    def save_to_db(self):
        pass