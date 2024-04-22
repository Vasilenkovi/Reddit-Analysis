from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect

def select_in_shortcut(database_dict: dict, f_query: str, params: dict, in_params: list):
    """Shortcut for variable length IN queries in injection-safe manner. \n
        parameters: \n
        \t database_dict - dict with db connection info. \n
        \t f_query - query as f-string where {in_expr} will be replaced with IN (...). \n
        \t params - regular parameters for query. This dict will be modified with in_params values. \n
        \t in_params - list of IN expression values. \n
        """

    in_expr = "IN ( "

    wrapped = []
    for s in in_params:
        params[s] = s
        wrapped.append(f"%({s})s")

    in_expr += ", ".join(wrapped) +" )"

    query = f_query.format(in_expr = in_expr)

    return execute(database_dict, query, params)


def execute(database_dict: dict, query: str, params: dict) -> list[tuple]:

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

    return execute(NATIVE_SQL_DATABASES['job_id'], query, params)

def get_user_datasets(limit: int = 100, offset: int = 0) -> list[tuple]:
    query = """SELECT task_id, query, created_timestamp FROM reddit_job_id.parsing_subreddits_id LIMIT %(limit)s OFFSET %(offset)s"""
    params = {
        "offset": offset,
        "limit": limit
    }

    return execute(NATIVE_SQL_DATABASES['job_id'], query, params)