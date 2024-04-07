from .Vectorizer import Vectorizer
from .Aglomerative import AgloDivMethod
from .Optics import Optics
from DjangoRed.settings import NATIVE_SQL_DATABASES

def clusterize(**kwargs):
    bd_conf = NATIVE_SQL_DATABASES['clustering_read']
    vc = Vectorizer(bd_conf=bd_conf)
    vc.get_doc_to_doc(kwargs["dataset_id"], kwargs["reduct_method"], kwargs["lang"], kwargs["distance"])
    if(kwargs["method"]=="Aglo" or kwargs["method"]=="Div"):
        adm = AgloDivMethod(vc.truncated[kwargs["reduct_method"]])
        adm.cluster(kwargs["method"],kwargs["distance"], kwargs["cluster_count"])
        return (adm.result, vc.truncated[kwargs["reduct_method"]])



def __init__():
    pass