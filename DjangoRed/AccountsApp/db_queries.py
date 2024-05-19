from ParserApp.forms import Form_types
from DjangoRed.settings import NATIVE_SQL_DATABASES
from mysql.connector import Connect
from json import loads


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

def chekc_for_exsisting_datasets():
    cnx = Connect(**NATIVE_SQL_DATABASES['job_id'])

    query = """SELECT FROM reddit_job_id.{safe_table_name}(query, created_timestamp) 
            VALUES (%(query)s, FROM_UNIXTIME(%(timestamp)s))""".format(safe_table_name = table_name)

    # cnx = Connect(**database_dict)
    # cur = cnx.cursor()
    # cur.reset()

    # cur.execute(query, params = params)
    # r = cur.fetchall()
    # cnx.close()

    return r