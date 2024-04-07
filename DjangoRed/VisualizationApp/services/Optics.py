from sklearn.cluster import OPTICS
import numpy as np
class Optics:
    def __init__(self,doc_to_doc_matrix):
        self.doc_to_doc_matrix = doc_to_doc_matrix
    def cluster(self):
        X = np.array(self.doc_to_doc_matrix)
        clustering = OPTICS().fit(X)
        self.save_to_db()
        return clustering
    def save_to_db(self):
        pass