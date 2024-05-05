from ParserApp.forms import Form_types
from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect
from json import loads

def select_in_shortcut(database_dict: dict, f_query: str, params: dict, in_params: list) -> list[tuple]:
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

def select_in_limit(database_dict: dict, f_query: str, params: dict, in_params: list, limit: int = 1000, offset: int = 0) -> list[tuple]:
    """Shortcut for variable length IN queries in injection-safe manner. \n
        parameters: \n
        \t database_dict - dict with db connection info. \n
        \t f_query - query as f-string where {in_expr} will be replaced with IN (...) and {limit} and {offset} will be substituted. \n
        \t params - regular parameters for query. This dict will be modified with in_params values. \n
        \t in_params - list of IN expression values. \n
        """

    in_expr = "IN ( "

    wrapped = []
    for s in in_params:
        params[s] = s
        wrapped.append(f"%({s})s")

    in_expr += ", ".join(wrapped) +" )"

    query = f_query.format(
        in_expr = in_expr,
        limit = limit,
        offset = offset
    )

    return execute(database_dict, query, params)

def execute(database_dict: dict, query: str, params: dict) -> list[tuple]:

    cnx = Connect(**database_dict)
    cur = cnx.cursor()
    cur.reset()

    cur.execute(query, params = params)
    r = cur.fetchall()
    cnx.close()

    return r

def execute_insert(database_dict: dict, query: str, params: dict) -> list[tuple]:

    cnx = Connect(**database_dict)
    cur = cnx.cursor()
    cur.reset()

    cur.execute(query, params = params)
    cnx.commit()
    cnx.close()

def get_comment_datasets(limit: int = 100, offset: int = 0) -> list[tuple]:
    query = """SELECT task_id, query, created_timestamp FROM reddit_job_id.parsing_comment_id LIMIT %(limit)s OFFSET %(offset)s"""
    params = {
        "offset": offset,
        "limit": limit
    }

    r = execute(NATIVE_SQL_DATABASES['job_id'], query, params)

    r_transform = map(
        lambda x: (x[0], __job_id_query_html_convert(x[1]), x[2]),
        r
    )

    return list(r_transform)

def get_user_datasets(limit: int = 100, offset: int = 0) -> list[tuple]:
    query = """SELECT task_id, query, created_timestamp FROM reddit_job_id.parsing_subreddits_id LIMIT %(limit)s OFFSET %(offset)s"""
    params = {
        "offset": offset,
        "limit": limit
    }

    r = execute(NATIVE_SQL_DATABASES['job_id'], query, params)
    r_transform = map(
        lambda x: (x[0], __job_id_query_html_convert(x[1]), x[2]),
        r
    )

    return list(r_transform)

def __job_id_query_html_convert(query_dict: str) -> dict:
    query_dict = loads(query_dict)
    form_type = query_dict["form_type"]
    r = {
        "type": form_type,
        "context": ""
    }

    match Form_types(form_type):
        case Form_types.COMMENT_SUBMISSION:
            conttext_str = __str_or_join_list(query_dict["submission_url"])
            r["context"] = conttext_str

        case Form_types.COMMENT_SUBREDDIT:
            conttext_str = __str_or_join_list(query_dict["subreddit_name"])
            r["context"] = conttext_str

        case Form_types.USERS:
            conttext_str = __str_or_join_list(query_dict["multi_subreddit_name"])
            r["context"] = conttext_str

    return r

def __str_or_join_list(str_or_list: str | list) -> str:
    if type(str_or_list) == str:
        return str_or_list
    
    return "; ".join(str_or_list)