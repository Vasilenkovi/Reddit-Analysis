import json
from channels.generic.websocket import WebsocketConsumer
from VisualizationApp.services import clusterize
class ClusterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
                'type':'connection_established',
             'message': "Connected!!"
            }
        ))
    def receive(self, text_data=None, bytes_data=None):
        received_message = json.loads(text_data)
        dataset_id = "prsc_1"#received_message["dataset_id"]
        methods = {'1':"SVD",'2':"TSNE"}
        langs = {'1':"english",'2':"russian"}
        dists = {'1':"cosine",'2':"euclidean"}
        methods_clust = {'1':"Aglo",'2':"Div",'3':"OPTICS"}
        cluster_count = int(received_message["clasters_count"])
        method = methods_clust[received_message["clasterization_method"]]
        lang = langs[received_message["language"]]
        reduct_method = methods[received_message["downsising_method"]]
        distance = dists[received_message["measure_of_distance"]]
        print(received_message)
        res = clusterize(dataset_id=dataset_id, method=method,lang=lang,reduct_method=reduct_method, distance=distance, cluster_count=cluster_count)
        labels = res[0]
        points = res[1]
        for i in range(len(labels)):
            self.send(text_data=json.dumps({
                'type': 'point message',
                'point': "{} {} {}".format(points[i][0], points[i][1], points[i][2]),
                'label': str(labels[i])
            }
            ))
    def disconnect(self, close_code):
        print(close_code)