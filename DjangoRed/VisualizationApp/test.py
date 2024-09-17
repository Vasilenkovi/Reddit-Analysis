from VisualizationApp.consumer import ClusterConsumer
from django.test import SimpleTestCase
from django.test import TestCase
from VisualizationApp.services import query_generator
import json

class test_receiver(SimpleTestCase):
    def setUp(self):
        self.test_miss = [
            json.loads('{ "clasters_count": "", "clasterization_method": 1, "language": 2, "downsising_method" : 2, "datasets" : "lp", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": 132, "clasterization_method": "", "language": 2, "downsising_method" : 2, "datasets" : "lp", "measure_of_distance" : 1}'),

            json.loads(
                '{ "clasters_count": 123, "clasterization_method": 1, "language": "", "downsising_method" : 2, "datasets" : "lp", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": 123, "clasterization_method": 1, "language": 2, "downsising_method" : "", "datasets" : "lp", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": 123, "clasterization_method": 1, "language": 2, "downsising_method" : 2, "datasets" : "", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": 123, "clasterization_method": 1, "language": 2, "downsising_method" : 2, "datasets" : "lp", "measure_of_distance" : ""}'),
            json.loads(
                '{ "clasters_count": "", "clasterization_method": "", "language": 2, "downsising_method" : 2, "datasets" : "lp", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": 34, "clasterization_method": "", "language": 2, "downsising_method" : 2, "datasets" : "", "measure_of_distance" : 1}'),

        ]
        self.test_wrong =[
            json.loads(
                '{ "clasters_count": "asd", "clasterization_method": "1", "language": "2", "downsising_method" : "2", "datasets" : "lp", "measure_of_distance" : "1"}'),
            json.loads(
                '{ "clasters_count": 2, "clasterization_method": "123", "language": "2", "downsising_method" : "2", "datasets" : "lp", "measure_of_distance" : "1"}'),
            json.loads(
                '{ "clasters_count": "32", "clasterization_method": 1, "language": "2", "downsising_method" : "2", "datasets" : "lp", "measure_of_distance" : "1"}'),
            json.loads(
                '{ "clasters_count": "34", "clasterization_method": "1", "language": "2", "downsising_method" : "hjkl89", "datasets" : "lp", "measure_of_distance" : 1}'),
            json.loads(
                '{ "clasters_count": "45", "clasterization_method": "1", "language": "2", "downsising_method" : "2", "datasets" : "lp", "measure_of_distance" : "6hk5"}')

        ]
        self.test_normal = [
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "1", "language": "2", "downsising_method" : "1", "datasets" : "lp12s3123", "measure_of_distance" : "1"}'),
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "2", "language": "1", "downsising_method" : "2", "datasets" : "lsdfg234p", "measure_of_distance" : "2"}'),
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "1", "language": "2", "downsising_method" : "1", "datasets" : "ls1412s1p", "measure_of_distance" : "2"}'),
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "2", "language": "1", "downsising_method" : "2", "datasets" : "lasgfasgdfasdgp", "measure_of_distance" : "1"}'),
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "1", "language": "2", "downsising_method" : "2", "datasets" : "lp", "measure_of_distance" : "2"}'),
            json.loads(
                '{ "clasters_count": 213, "clasterization_method": "2", "language": "2", "downsising_method" : "1", "datasets" : "lp", "measure_of_distance" : "1"}'),
        ]


    def test_receive_wrong_data(self): # If received wrong data method must raise an error
        for i in self.test_wrong:
            with self.assertRaises(Exception ):
                result = ClusterConsumer.receive_transform(i)

    def test_receive_missing_data(self): #
        for i in self.test_miss:
            with self.assertRaises(Exception):
                result = ClusterConsumer.receive_transform(i)
    def test_receive_check_transform_format(self): #
        for i in self.test_normal:
            result = ClusterConsumer.receive_transform(ClusterConsumer, i)
            self.assertEqual(type(result['distance']), str)
            self.assertEqual(type(result['method']), str)
            self.assertEqual(type(result['lang']), str)
            self.assertEqual(type(result['reduct_method']), str)
            self.assertEqual(type(result['cluster_count']), int)

class test_queue_gen(TestCase):
    def setUp(self):
        self.wrong_data = [
            {"job_id": "elf.job_id", "dataset_id" : 12, "method":"self.method", "lang" : "self.lang",
             "reduct_method": "self.reduct_method", "distance" : "self.distance", "cluster_count": 12},
        ]
        self.correct_data = [
            {"job_id": "elf.job_id", "dataset_id": "id", "method": "self.method", "lang": "self.lang",
             "reduct_method": "self.reduct_method", "distance": "self.distance", "cluster_count": 12},
        ]
    def test_receive_wrong_data(self):
        for i in self.wrong_data:
            with self.assertRaises(Exception):
                print(i)
                query_generator(i)
    def test_receive_correct_data(self):
        for i in self.correct_data:
            res = query_generator(i)
            self.assertIsNotNone(res)
            queue_check, check_params, query_to_add, addition_params, queue_get_coordinates, get_coords_params, job_id = res
            self.assertEqual(type(queue_check), str)
            self.assertEqual(type(check_params), dict)
            self.assertEqual(type(query_to_add), str)
            self.assertEqual(type(addition_params), dict)
            self.assertEqual(type(queue_get_coordinates), str)
            self.assertEqual(type(get_coords_params), dict)
            self.assertEqual(type(job_id), str)




from VisualizationApp.services.Assessment import assessor
import pickle
class assesment_test(SimpleTestCase):

    def setUp(self):
        self.data = []
        # with open('C:/Users/Vizor/Desktop/Учеба/4 course/Reddit-Analysis/DjangoRed/VisualizationApp/services/listfile', 'rb') as fp:
        #     self.data = pickle.load(fp)
        with open('./VisualizationApp/services/listfile', 'rb') as fp:
            self.data = pickle.load(fp)

    def test_check_calculation(self):
        for i in self.data:
            n, lbs_count, coord, labels, res = i
            a = assessor(labels, coord, lbs_count)
            self.assertTrue(abs(a.siluet()-res[0])<0.001)
            self.assertTrue(abs(a.cohesion()-res[1])<0.001)
            self.assertTrue(abs(a.separation(n)-res[2])<0.001)