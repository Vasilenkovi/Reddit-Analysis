from django import forms
from django.contrib.auth.models import User

CLASTERIZATION_CHOICES =( 
    ("1", "Aglomerative"), 
    ("2", "Divisionary"), 
    ("3", "OPTICS"),
)

LANGUAGES = (
    ("1", "English"),
    ("2", "Russian")
)

DOWNSIZING_METHODS = (
    ("1", "SVD"),
    ("2", "TSNE")
)
MEASURES_OF_DISTANCE = (
    ("1", "cos"),
    ("2", "euclid")
)

class VisualizationForm(forms.Form):
    dataset_id = forms.CharField(max_length=12)
    clasterization_method = forms.MultipleChoiceField(choices=CLASTERIZATION_CHOICES)
    clasters_count = forms.IntegerField()
    language = forms.MultipleChoiceField(choices=LANGUAGES)
    downsising_method = forms.MultipleChoiceField(choices=DOWNSIZING_METHODS)
    measure_of_distance = forms.MultipleChoiceField(choices=MEASURES_OF_DISTANCE)


# ID - запроса данных
# JS-Message1: Метод кластеризации[Aglomerative, Divisionary, OPTICS], количество кластеров(только для Aglomerative и Divisionary), язык[Russian, English], метод снижения размерности[SVD, TSNE], мера расстояния[cos, euclid]
# Single-Message1
# Server-Response1: "Begin"
# [1,x,y,z]
# Server-Responsen: "End"

# BatchMessage:
# Server-Response1: "Begin"
# [[1,x,y,z],....]
# Server-Responsen: "End"

# FullMessage
# [[1,x,y,z],....] 