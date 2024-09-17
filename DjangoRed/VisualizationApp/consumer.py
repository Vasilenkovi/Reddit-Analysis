import json
from channels.generic.websocket import WebsocketConsumer
from VisualizationApp.services import clusterize
from IdApp.task_id_manager import get_task_id, Job_types
class ClusterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
                'type':'connection_established',
             'message': "Connected!!"
            }
        ))
    def receive_transform(self, received_message):
        self.dataset_id = received_message["datasets"]
        methods = {'1': "SVD", '2': "TSNE"}
        langs = {'1': "english", '2': "russian"}
        dists = {'1': "cosine", '2': "euclidean"}
        methods_clust = {'1': "Aglo", '2': "Div", '3': "OPTICS"}
        self.cluster_count = int(received_message["clasters_count"])
        self.method = methods_clust[received_message["clasterization_method"]]
        self.lang = langs[received_message["language"]]
        self.reduct_method = methods[received_message["downsising_method"]]
        self.distance = dists[received_message["measure_of_distance"]]
        if self.cluster_count== None or self.method == None or self.lang == None or self.reduct_method == None or self.distance==None:
            raise Exception
        return {"distance": self.distance, "reduct_method": self.reduct_method, "lang": self.lang, "method": self.method, "cluster_count" : self.cluster_count}
    def receive_answer(self):
        try:
            res = clusterize(job_id=self.job_id, dataset_id=self.dataset_id, method=self.method, lang=self.lang, reduct_method=self.reduct_method, distance=self.distance, cluster_count=self.luster_count)
            labels = res[0]
            points = res[1]
            self.send(text_data=json.dumps({
                    'type': 'begin',
                }
            ))
            for i in range(len(labels)):
                self.send(text_data=json.dumps({
                    'type': 'point message',
                    'point': "[{}, {}, {}]".format(points[i][0], points[i][1], points[i][2]),
                    'label': str(labels[i])
                }
                ))
            self.send(text_data=json.dumps({
                    'type': 'end',
                }
                ))
        except Exception as e:
            self.send(
                text_data=json.dumps({
                    'type': 'error_message',
                    'error': str(e)
                }
                ))
        finally:
            return
    def receive(self, text_data=None, bytes_data=None):
        received_message = json.loads(text_data)
        self.job_id = get_task_id(Job_types.CLUSTER, text_data)
        self.receive_transform(received_message)
        self.receive_answer()

    def disconnect(self, close_code):
        print(close_code)