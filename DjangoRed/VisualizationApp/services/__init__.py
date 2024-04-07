from .Vectorizer import Vectorizer
from .Aglomerative import AgloDivMethod
from .Optics import Optics
from os import getcwd
from omegaconf import OmegaConf

def clusterize(**kwargs):
    print(kwargs)
    BASE_DIR = getcwd ()
    print(BASE_DIR)
    BASE_DIR= BASE_DIR.replace("\\","/")
    bd_conf = OmegaConf.load(BASE_DIR + "/DjangoRed/config/MySQL_local_clustering.yaml")
    vc = Vectorizer(bd_conf=bd_conf)
    vc.get_doc_to_doc(kwargs["dataset_id"], kwargs["reduct_method"], kwargs["lang"], kwargs["distance"])
    if(kwargs["method"]=="Aglo" or kwargs["method"]=="Div"):
        adm = AgloDivMethod(vc.truncated[kwargs["reduct_method"]])
        adm.cluster(kwargs["method"],kwargs["distance"], kwargs["cluster_count"])
        return (adm.result, vc.truncated[kwargs["reduct_method"]])



def __init__():
    pass