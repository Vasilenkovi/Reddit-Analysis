import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import UserAccount, FavoriteJobIDs

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
            user_id = received_message["user_id"]
            dataset_id = received_message["dataset_id"]
            user_reference = get_object_or_404(UserAccount, username=user_id)
            message = ''
            match (len(FavoriteJobIDs.objects.filter(job_id=dataset_id))):
                case (0):
                    new_favorite = FavoriteJobIDs(username=user_reference, job_id=dataset_id)
                    new_favorite.save()
                    message = f'Successfully added {dataset_id} to favorites'
                case(1):
                    message = f'{dataset_id} is already added to favorites'
                case _:
                    raise Exception("More than one entry of that dataset in the database")

            self.send(
                text_data=json.dumps({
                    'type': 'favorite_add_success',
                    'message': message
                })
            )


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