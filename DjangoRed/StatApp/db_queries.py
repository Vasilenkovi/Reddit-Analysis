from DjangoRed.settings import NATIVE_SQL_DATABASES
from IdApp.db_query import select_in_shortcut
import IdApp
from functools import partial
from mysql.connector import Connect, errors

def select_comment_dataset_from_ids(dataset_ids: list) -> list[tuple]:
    
    f_query = """ SELECT sc.text_body, s.full_name, s.title, s.upvotes, s.url
                  FROM reddit_parsing.submission_comment AS sc
                  JOIN reddit_parsing.submission AS s ON (sc.submission_name = s.full_name) AND (sc.job_id = s.job_id)
                  WHERE sc.job_id {in_expr}
                  ORDER BY s.upvotes
                  DESC; """

    return select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids)

def make_job(params: dict):
    query_job_id = """INSERT INTO statisticsdb.statistic(url, full_name, title, upvote, word_cloud, neg_count, pos_count, neg_com, pos_com, job_id)
        VALUES (%(url)s, %(full_name)s, %(title)s, %(upvote)s, %(word_cloud)s, %(neg_count)s, %(pos_count)s, %(neg_com)s, %(pos_com)s, %(job_id)s)"""
    
    IdApp.db_query.execute_insert(NATIVE_SQL_DATABASES['stat'], query_job_id, params)
