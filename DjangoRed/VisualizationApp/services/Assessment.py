from sklearn.metrics import silhouette_score

class assessor:
    def __init__(self, labels, coords, lbs_count):
        self.labels = labels
        self.coords = coords
        self.mean_x_for_labels = dict()
        self.mean_y_for_labels = dict()
        self.mean_z_for_labels = dict()
        self.labels_count = dict()
        self.lbs_count = lbs_count
        self.lbs_points = dict()
        for i in range(lbs_count):
            self.mean_z_for_labels[i] = 0
            self.mean_x_for_labels[i] = 0
            self.mean_y_for_labels[i] = 0
            self.labels_count[i] = 0
            self.lbs_points[i] = []
        for i in range(len(labels)):
            #print(i, len(labels), len(coords), labels[i], len(self.mean_x_for_labels) )

            self.mean_x_for_labels[labels[i]] += coords[i][0]
            self.mean_y_for_labels[labels[i]] += coords[i][1]
            self.mean_z_for_labels[labels[i]] += coords[i][2]
            self.labels_count[labels[i]] += 1
            self.lbs_points[labels[i]].append(coords[i])
        self.all_x_mean = 0
        self.all_y_mean = 0
        self.all_z_mean = 0
        for i in range(lbs_count):
            self.mean_x_for_labels[i] /= self.labels_count[i]
            self.mean_y_for_labels[i] /= self.labels_count[i]
            self.mean_z_for_labels[i] /= self.labels_count[i]
            self.all_x_mean += self.mean_x_for_labels[i]
            self.all_y_mean += self.mean_y_for_labels[i]
            self.all_z_mean += self.mean_z_for_labels[i]
        self.all_x_mean /= self.lbs_count
        self.all_y_mean /= self.lbs_count
        self.all_z_mean /= self.lbs_count
    def cohesion(self):
        WSS = 0
        for j in range(self.lbs_count):
            WSS_IN = 0
            for i in range(len(self.lbs_points)):

                WSS_IN += (self.lbs_points[i][0][0] - self.mean_x_for_labels[j])**2 +  (self.lbs_points[i][1][1] - self.mean_y_for_labels[j])**2 + (self.lbs_points[i][2][2] - self.mean_z_for_labels[j])**2
            WSS += WSS_IN
        return WSS
    def separation(self, n):
        BSS = 0
        for i in range(self.lbs_count):
            BSS += (self.mean_x_for_labels[i]-self.all_x_mean)**2 + \
                   (self.mean_y_for_labels[i]-self.all_y_mean)**2 + \
                   (self.mean_z_for_labels[i]-self.all_z_mean)**2
        BSS *= n
        return BSS
    def siluet(self):
        return silhouette_score(self.coords, self.labels)

# import random
# import pickle
# samples = []
# for i in range(10):
#     n = random.randint(1, 1000)
#     k = random.randint(0, n//10)
#     #print(k)
#     coords = []
#     labels = []
#     for j in range(n):
#         x = random.uniform(-1000, 1000)
#         y = random.uniform(-1000, 1000)
#         z = random.uniform(-1000, 1000)
#         label = random.randint(0, k-1)
#         #print(label, k)
#         coords.append([x,y,z])
#         labels.append(label)
#     a = assessor(labels, coords, k)
#     cohesion_score = a.cohesion()
#     separation_score = a.separation(n)
#     sil = a.siluet()
#     sample = (n, k, coords, labels, [sil, cohesion_score, separation_score])
#     samples.append(sample)
# with open('listfile', 'wb') as fp:
#     pickle.dump(samples, fp)
#     print('Done writing list into a binary file')