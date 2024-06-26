from django import forms
from django.contrib.auth.models import User

ID_CHOICES =( 
    ("1", "A12421"), 
    ("2", "B213wer1"), 
    ("3", "Hue"),
)

CLASTERIZATION_CHOICES =( 
    ("1", "Aglomerative"), 
    ("2", "Divisionary"), 
    ("3", "OPTICS"),
)

LANGUAGES_CHOICES = (
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
    
    clasterization_method = forms.ChoiceField(choices=CLASTERIZATION_CHOICES)
    clasters_count = forms.IntegerField(min_value=1, max_value=10)
    language = forms.ChoiceField(choices=LANGUAGES_CHOICES)
    downsising_method = forms.ChoiceField(choices=DOWNSIZING_METHODS)
    measure_of_distance = forms.ChoiceField(choices=MEASURES_OF_DISTANCE)


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