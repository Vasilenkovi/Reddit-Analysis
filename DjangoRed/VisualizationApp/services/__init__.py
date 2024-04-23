from .Vectorizer import Vectorizer
from .Aglomerative import AgloDivMethod
from .Optics import Optics
from DjangoRed.settings import NATIVE_SQL_DATABASES
from IdApp.db_query import execute
import pickle
def clusterize(**kwargs):
    bd_conf_read = NATIVE_SQL_DATABASES['clustering_read']
    bd_conf_save = NATIVE_SQL_DATABASES['clustering_saving']
    job_id = kwargs["job_id"]
    queue_check = "SELECT Labels from clusteringdb.clustresult where  command=%(cmd)s"
    command = kwargs["method"] + kwargs["reduct_method"] + kwargs["distance"] + str(kwargs["cluster_count"]+kwargs["lang"])
    check_params = {
        "cmd" : command
    }
    check_result = execute(bd_conf_save, queue_check, check_params)
    query_to_add = "INSERT clusteringdb.clustresult (Labels, command, JobID, DataSet) values(%(labs)s, %(cmd)s, %(jid)s, %(dts)s); COMMIT;"
    addition_params = {
        "labs": None,
        "jid": job_id,
        "cmd": command,
        "dts": "|".join(kwargs["dataset_id"])
    }
    if len(check_result) == 0:
        vc = Vectorizer(bd_conf_read=bd_conf_read, bd_conf_save=bd_conf_save, job_id=job_id)
        vc.get_doc_to_doc(kwargs["dataset_id"], kwargs["reduct_method"], kwargs["lang"])
        if(kwargs["method"]=="Aglo" or kwargs["method"]=="Div"):
            adm = AgloDivMethod(vc.truncated[kwargs["reduct_method"]])
            adm.cluster(kwargs["method"],kwargs["distance"], kwargs["cluster_count"])
            addition_params["labs"] = pickle.dumps(adm.result)
            insert_resp = execute(bd_conf_save, query_to_add, addition_params)
            return (adm.result, vc.truncated[kwargs["reduct_method"]])
        if(kwargs["method"]=="OPTICS"):
            opt = Optics(vc.truncated[kwargs["reduct_method"]])
            addition_params["labs"] = pickle.dumps(opt.result)
            insert_resp = execute(bd_conf_save, query_to_add, addition_params)
            return (opt.cluster(), vc.truncated[kwargs["reduct_method"]])
    else:
        queue_get_coordinates = "SELECT %(method)s from clusteringdb.clustdata where DataSet = %(dts)s;"
        get_coords_params = {
            "method": kwargs["reduct_method"],
            "dts": "|".join(kwargs["dataset_id"])
        }
        coord_query_res = execute(bd_conf_save, queue_get_coordinates, get_coords_params)
        print("labels",check_result)
        print("coords",coord_query_res)
        return (pickle.loads(check_result[0][0]), pickle.loads(coord_query_res[0][0]))



def __init__():
    pass