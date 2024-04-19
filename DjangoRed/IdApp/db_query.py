from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect

def _execute(database_dict: dict, query: str, params: dict) -> list[tuple]:

    cnx = Connect(**database_dict)
    cur = cnx.cursor()
    cur.reset()

    cur.execute(query, params = params)
    r = cur.fetchall()
    cnx.close()

    return r

def get_comment_datasets(limit: int = 100, offset: int = 0) -> list[tuple]:
    query = """SELECT task_id, query, created_timestamp FROM reddit_job_id.parsing_comment_id LIMIT %(limit)s OFFSET %(offset)s"""
    params = {
        "offset": offset,
        "limit": limit
    }

    return _execute(NATIVE_SQL_DATABASES['job_id'], query, params)

def get_user_datasets(limit: int = 100, offset: int = 0) -> list[tuple]:
    query = """SELECT task_id, query, created_timestamp FROM reddit_job_id.parsing_subreddits_id LIMIT %(limit)s OFFSET %(offset)s"""
    params = {
        "offset": offset,
        "limit": limit
    }

    return _execute(NATIVE_SQL_DATABASES['job_id'], query, params)