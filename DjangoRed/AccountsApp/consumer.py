import json
from channels.generic.websocket import WebsocketConsumer

class FavConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_success',
            'message': 'Connection established'
        }))

    def receive(self, text_data=None, bytes_data=None):
        received_message = json.loads(text_data)
        try:
            cookies = received_message["cookies"]
            dataset_id = received_message["dataset_id"]
            print(f"cookies: {cookies} \n dataset_id: {dataset_id}")

        except Exception as e:
            self.send(
                text_data=json.dumps({
                    'type': 'error_message',
                    'error': str(e)
                }
                ))
        # received_message = json.loads(text_data)
        # try:
        #     dataset_id = received_message["datasets"]
        #     methods = {'1':"SVD",'2':"TSNE"}
        #     langs = {'1':"english",'2':"russian"}
        #     dists = {'1':"cosine",'2':"euclidean"}
        #     methods_clust = {'1':"Aglo",'2':"Div",'3':"OPTICS"}
        #     cluster_count = int(received_message["clasters_count"])
        #     method = methods_clust[received_message["clasterization_method"]]
        #     lang = langs[received_message["language"]]
        #     reduct_method = methods[received_message["downsising_method"]]
        #     distance = dists[received_message["measure_of_distance"]]
        #     job_id = get_task_id(Job_types.CLUSTER, text_data)
        #     res = clusterize(job_id=job_id, dataset_id=dataset_id, method=method, lang=lang, reduct_method=reduct_method, distance=distance, cluster_count=cluster_count)
        #     labels = res[0]
        #     points = res[1]
        #     self.send(text_data=json.dumps({
        #             'type': 'begin',
        #         }
        #     ))
        #     for i in range(len(labels)):
        #         self.send(text_data=json.dumps({
        #             'type': 'point message',
        #             'point': "[{}, {}, {}]".format(points[i][0], points[i][1], points[i][2]),
        #             'label': str(labels[i])
        #         }
        #         ))
        #     self.send(text_data=json.dumps({
        #             'type': 'end',
        #         }
        #         ))
        # except Exception as e:
        #     self.send(
        #         text_data=json.dumps({
        #             'type': 'error_message',
        #             'error': str(e)
        #         }
        #         ))

    def disconnect(self, close_code):
        print(close_code)