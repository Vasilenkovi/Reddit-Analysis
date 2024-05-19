from ParserApp.forms import Form_types
from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect
from json import loads


def check_for_up_to_date_job_ids():
    cnx = Connect(**NATIVE_SQL_DATABASES['job_id'])
    
    job_ids = []
    queries = [
        f"""SELECT task_id FROM reddit_job_id.parsing_comment_id;""",
        f"""SELECT task_id FROM reddit_job_id.clustering_id;""",
        f"""SELECT task_id FROM reddit_job_id.parsing_subreddits_id;"""
    ]
    
    cur = cnx.cursor()
    for query in queries:
        cur.reset()        
        cur.execute(query)
        r = cur.fetchall()
        for tup in r:
            job_ids.append(tup[0])
    
    cnx.close()

    return job_ids