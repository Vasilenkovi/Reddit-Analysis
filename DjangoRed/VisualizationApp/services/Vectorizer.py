from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize
import nltk
#nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from .russian_stemmer import *
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
import mysql.connector
from mysql.connector import Error
import numpy as np
import pickle
import scipy as sp
from IdApp.db_query import execute
class LSA:
    def normalization(language, item):
        list_of_tokens = item.split()
        normalized_list = []
        if (language == "русский"):
            morph = Stemmer()
            for i in list_of_tokens:
                normalized_list.append(morph.stem(word=i))
        else:
            morph = WordNetLemmatizer()
            for i in list_of_tokens:
                normalized_list.append(morph.lemmatize(i))
        Set = list(set(normalized_list))
        Set.sort()
        res = ""
        for i in Set:
            res += i + " "
        return res

    def LSA_SVD(matrix, k):
        svd = TruncatedSVD(n_components=k)
        print(type(matrix), "type of matrix")
        matrix_scaled = svd.fit_transform(matrix)
        return matrix_scaled

    def LSA_T_SNE(matrix, k=3):
        X_embedded = TSNE(n_components=k, learning_rate='auto',
        init = 'random', perplexity = 3).fit_transform(matrix)
        return X_embedded

    def calculate_distance(vector1, vector2):
        len1 = 0
        for i in vector1:
            len1 += i ** 2
        len1 = math.sqrt(len1)
        len2 = 0
        for i in vector2:
            len2 += i ** 2
        len2 = math.sqrt(len2)
        cosbtw = 0
        for i in range(len(vector1)):
            cosbtw += vector1[i] * vector2[i]
        cosbtw /= (len1 * len2)
        return cosbtw

    def get_doc_to_doc_table(matrix, method):
        table = [[-1] * len(matrix)] * len(matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if (i != j):
                    table[i][j] = LSA.calculate_distance(matrix[i], matrix[j])
        return table



class Vectorizer:
    def __init__(self, bd_conf_read, bd_conf_save, job_id):
        self.corpus = []
        self.bd_conf_read = bd_conf_read
        self.bd_conf_save = bd_conf_save
        self.truncated = {"SVD": None, "TSNE": None}
        self.vectorized = None
        self.doc_to_doc = None
        self.job_id = job_id
    def _collect_corpus(self, language, dataset_id):
        try:
            conn = mysql.connector.connect(host=self.bd_conf_read["host"],
                                           database=self.bd_conf_read["database"],
                                           user=self.bd_conf_read["user"],
                                           password=self.bd_conf_read["password"])
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute("SELECT text_body FROM submission_comment WHERE job_id=\'"+dataset_id+"\';")
            row = cursor.fetchone()
            while row is not None:
                row = cursor.fetchone()
                if row!=None:
                    self.corpus.append(row[0])
        except Error as e:
            print(e)
        else:
            conn.close()

    def _vectorize(self, dataset_id):
        checking_query = """SELECT Vector FROM clusteringdb.clustdata WHERE DataSet=%(dataset_id)s;"""
        checking_params = {"dataset_id": "|".join(dataset_id)}
        checking_result = execute(self.bd_conf_save, checking_query, checking_params)
        if len(checking_result)==0:
            vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
            X = vectorizer.fit_transform(self.corpus)
            print(type(X), "type of X")
            S = X
            self.vectorized = X
            blob_vectorized = pickle.dumps(S)
            insert_query = """INSERT clusteringdb.clustdata(DataSet, Vector) values  ( %(JobID)s, %(VectorBlob)s); COMMIT;"""
            insert_params = {
                "JobID": "|".join(dataset_id),
                "VectorBlob": blob_vectorized
            }
            insert_result = execute(self.bd_conf_save, insert_query, insert_params)
        else:
            temp = pickle.loads(checking_result[0][0])
            self.vectorized = temp


    def _reduce_dimens(self, method, dataset_id):
        k=3
        checking_query = """SELECT %(mth)s FROM clusteringdb.clustdata WHERE DataSet=%(dataset_id)s; COMMIT;"""
        checking_params = {
            "mth" : method,
            "dataset_id": "|".join(dataset_id)
        }
        checking_result = execute(self.bd_conf_save, checking_query, checking_params)
        if len(checking_result[0])==1:
            if(method=="SVD"):
                self.truncated["SVD"] = LSA.LSA_SVD(self.vectorized, k)
            else:
                self.truncated["TSNE"] = LSA.LSA_T_SNE(self.vectorized, k)
            insert_query = """UPDATE clusteringdb.clustdata set """+method+""" = (%(VectorBlob)s) where DataSet = %(DataSets)s ; COMMIT;"""
            insert_params = {
                "mth" : method,
                "VectorBlob": pickle.dumps(self.truncated[method]),
                "DataSets": "|".join(dataset_id)
            }
            insert_result = execute(self.bd_conf_save, insert_query, insert_params)
        else:
            self.truncated[method] = pickle.loads(checking_result[0][0])




    def get_doc_to_doc(self, dataset_id, reduce_method, language):
        self._collect_corpus(language, dataset_id)
        self._vectorize(dataset_id)
        self._reduce_dimens(reduce_method, dataset_id)
