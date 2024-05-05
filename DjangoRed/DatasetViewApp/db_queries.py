from DjangoRed.settings import NATIVE_SQL_DATABASES
from IdApp.db_query import select_in_shortcut, select_in_limit

def select_comment_dataset_from_ids(dataset_ids: list) -> tuple[list, list]:

    headers = ["dataset id", "comment full name", "parent submission full name", "comment text body", "comment author", "comment rating", 
                       "comment creation timestamp", "comment parsing timestamp", "parent submission url", "parent submission title", "parent submisiion text body",
                       "parent submission author", "parent submission rating", "parent submission creation timestamp", "parent submission parsing timestamp", "parent submission flair"]

    f_query = """SELECT sc.job_id, sc.full_name, sc.submission_name, sc.text_body, sc.author, sc.upvotes, sc.created_timestamp, 
                    sc.parsed_timestamp, s.url, s.title, s.text_body, s.author, s.upvotes, s.created_timestamp, s.parsed_timestamp, s.flair 
                    FROM reddit_parsing.submission_comment AS sc 
                    JOIN reddit_parsing.submission AS s ON (sc.submission_name = s.full_name) AND (sc.job_id = s.job_id)
                    WHERE sc.job_id {in_expr};"""
    
    return (select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids), headers)

def select_comment_dataset_from_ids_limit(dataset_ids: list, limit: int = 1000, offset: int = 0) -> tuple[list, list, int]:

    headers = ["dataset id", "comment full name", "parent submission full name", "comment text body", "comment author", "comment rating", 
                       "comment creation timestamp", "comment parsing timestamp", "parent submission url", "parent submission title", "parent submisiion text body",
                       "parent submission author", "parent submission rating", "parent submission creation timestamp", "parent submission parsing timestamp", "parent submission flair"]

    f_query = """SELECT sc.job_id, sc.full_name, sc.submission_name, sc.text_body, sc.author, sc.upvotes, sc.created_timestamp, 
                    sc.parsed_timestamp, s.url, s.title, s.text_body, s.author, s.upvotes, s.created_timestamp, s.parsed_timestamp, s.flair 
                    FROM reddit_parsing.submission_comment AS sc 
                    JOIN reddit_parsing.submission AS s ON (sc.submission_name = s.full_name) AND (sc.job_id = s.job_id)
                    WHERE sc.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
    
    count_query = """SELECT count(sc.full_name) 
                    FROM reddit_parsing.submission_comment AS sc 
                    JOIN reddit_parsing.submission AS s ON (sc.submission_name = s.full_name) AND (sc.job_id = s.job_id)
                    WHERE sc.job_id {in_expr};"""

    total = select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], count_query, {}, dataset_ids)[0][0]
    
    return (select_in_limit(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids, limit, offset), headers, total)

def sub_select_comment_dataset_from_ids(columns: list, dataset_ids: list) -> list[tuple]:
    
    f_query_cols = """SELECT {cols} 
                    FROM reddit_parsing.submission_comment AS sc 
                    JOIN reddit_parsing.submission AS s ON (sc.submission_name = s.full_name) AND (sc.job_id = s.job_id)
                    WHERE sc.job_id {in_expr};"""
    
    f_query = f_query_cols.format(cols = ", ".join(columns), in_expr = "{in_expr}")
    
    return select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids)

def select_user_dataset_from_ids(dataset_ids: list) -> tuple[list, list]:

    headers = ["dataset id", "user full name", "subreddit full name", "parsed timestamp", "displayed subreddit name", "subreddi url"]

    f_query = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr};"""
    
    return (select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids), headers)

def select_user_dataset_from_ids_limit(dataset_ids: list, limit: int = 1000, offset: int = 0) -> tuple[list, list]:

    headers = ["dataset id", "user full name", "subreddit full name", "parsed timestamp", "displayed subreddit name", "subreddi url"]

    f_query = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
    
    count_query = """SELECT count(su.user_full_name)
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr};"""

    total = select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], count_query, {}, dataset_ids)[0][0]
    
    return (select_in_limit(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids, limit, offset), headers, total)

def sub_select_user_dataset_from_ids(columns: list, dataset_ids: list) -> list[tuple]:

    f_query_cols = """SELECT {cols}
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr};"""
    
    f_query = f_query_cols.format(cols = ", ".join(columns), in_expr = "{in_expr}")
    
    return select_in_shortcut(NATIVE_SQL_DATABASES['dataset_reader'], f_query, {}, dataset_ids)