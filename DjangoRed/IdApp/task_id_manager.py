from mysql.connector import Connect
from DjangoRed.settings import NATIVE_SQL_DATABASES
from json import dumps
import time

class Job_types:
    PARSE_COMMENTS = "prsc"
    PARSE_SUBREDDITS = "prsr"
    CLUSTER = "clus"

class Valid_tables:
    PARSING_COMMENT_ID = "PARSING_COMMENT_ID"
    PARSING_SUBREDDITS_ID = "PARSING_SUBREDDITS_ID"
    CLUSTERING_ID = "CLUSTERING_ID"

def get_task_id(job: Job_types, query: dict) -> str:
    match job:
        case Job_types.PARSE_COMMENTS:
            return __mysql_query(Job_types.PARSE_COMMENTS, Valid_tables.PARSING_COMMENT_ID, query)

        case Job_types.PARSE_SUBREDDITS:
            return __mysql_query(Job_types.PARSE_SUBREDDITS, Valid_tables.PARSING_SUBREDDITS_ID, query)
            
        case Job_types.CLUSTER:
            return __mysql_query(Job_types.CLUSTER, Valid_tables.CLUSTERING_ID, query)

        case _:
            raise AttributeError("Unregistered job type. Consult task_id_manager.Job_types")
            
def __mysql_query(job_type: Job_types, table_name: Valid_tables, in_query: dict) -> str:
    if table_name not in vars(Valid_tables).keys():
        raise AttributeError("Unsupported table name")

    cnx = Connect(**NATIVE_SQL_DATABASES['job_id'])
    cur = cnx.cursor()
    cur.reset()

    query = """INSERT INTO reddit_job_id.{safe_table_name}(query, created_timestamp) 
            VALUES (%(query)s, FROM_UNIXTIME(%(timestamp)s))""".format(safe_table_name = table_name)
    cur.execute(query, params = {
        'query': dumps(in_query),
        'timestamp': int(time.time())
    })
    cur.reset()

    query = """SELECT LAST_INSERT_ID()"""
    cur.execute(query)
    psysical_id = cur.fetchall()[0][0]
    cur.reset()

    new_task_id = job_type + "_" + str(psysical_id)

    query = """UPDATE reddit_job_id.{safe_table_name} 
            SET task_id = %(new_task_id)s
            WHERE id = %(new_id)s""".format(safe_table_name = table_name)
    cur.execute(query, params = {
        'new_task_id': new_task_id,
        'new_id': psysical_id
    })
    cur.reset()

    cnx.commit()
    cnx.close()

    return new_task_id