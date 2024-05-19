from ParserApp.forms import Form_types
from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect
from json import loads


# def get_user_favorite_jog_ids(limit: int = 100, offset: int = 0) -> list[tuple]:
#     query = """SELECT job_id from job_id where job_id = job_id"""

#     params = {
#         "offset": offset,
#         "limit": limit
#     }

def execute(database_dict: dict, query: str, params: dict) -> list[tuple]:

    cnx = Connect(**database_dict)
    cur = cnx.cursor()
    cur.reset()

    cur.execute(query, params = params)
    r = cur.fetchall()
    cnx.close()

    return r