from DjangoRed.settings import NATIVE_SQL_DATABASES
from IdApp.db_query import select_in_shortcut

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