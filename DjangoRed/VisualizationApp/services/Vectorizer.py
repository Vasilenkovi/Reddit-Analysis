from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from .russian_stemmer import *
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
import mysql.connector
from mysql.connector import Error
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
        matrix_scaled = svd.fit_transform(matrix)
        return matrix_scaled

    def LSA_T_SNE(matrix, k=2):
        sc = StandardScaler()
        X_scaled = sc.fit_transform(matrix)
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)
        tsne = TSNE(n_components=k)
        X_tsne = tsne.fit_transform(X_pca)
        return X_tsne

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
    def __init__(self, bd_conf):
        self.corpus = []
        self.bd_conf = bd_conf
        self.truncated = {"SVD": None, "TSNE": None}
        self.vectorized = None
        self.doc_to_doc = None
    def _collect_corpus(self, language, dataset_id):
        try:
            conn = mysql.connector.connect(host=self.bd_conf["host"],
                                           database=self.bd_conf["database_source"],
                                           user=self.bd_conf["user"],
                                           password=self.bd_conf["password"])
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
        finally:
            conn.close()

    def _vectorize(self):
        vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(self.corpus)
        self.vectorized = X
    def _reduce_dimens(self, method):
        k=3
        if(method=="SVD"):
            self.truncated["SVD"] = LSA.LSA_SVD(self.vectorized, k)
        else:
            self.truncated["TSNE"] = LSA.LSA_T_SNE(self.vectorized, k)
    def get_doc_to_doc(self, dataset_id, reduce_method, language, distance_type):
        k = 3
        self._collect_corpus(language, dataset_id)
        self._vectorize()
        #print(self.vectorized)
        self._reduce_dimens(reduce_method)
        #print(self.truncated["SVD"])
        #self.doc_to_doc = LSA.get_doc_to_doc_table(matrix=self.truncated[reduce_method], method=distance_type)
        #print(self.doc_to_doc)
        #self.save_to_db()
    def save_to_db(self):
        pass