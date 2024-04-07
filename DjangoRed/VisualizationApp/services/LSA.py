from nltk.stem import WordNetLemmatizer
import russian_stemmer
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
class LSA:
	def normalization(language,item):
		list_of_tokens = item.split()
		normalized_list = []
		if (language=="русский"):
			morph = russian_stemmer.Stemmer()
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
			res+=i+" "
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
			len1 += i**2
		len1 = math.sqrt(len1)
		len2 = 0
		for i in vector2:
			len2 += i ** 2
		len2 = math.sqrt(len2)
		cosbtw = 0
		for i in range(len(vector1)):
			cosbtw += vector1[i]*vector2[i]
		cosbtw /= (len1*len2)
		return cosbtw

	def get_doc_to_doc_table(matrix, method):
		table = [[-1]*len(matrix)]*len(matrix)
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				if(i!=j):
					table[i][j] = calculate_distance(matrix[i],matrix[j])
		return table
