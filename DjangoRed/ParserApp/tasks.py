from DjangoRed.settings import NATIVE_SQL_DATABASES, REDDIT_CLIENT
from celery import shared_task
from jsonpickle import encode, decode # Unsafe. Consider possible tampering
from .ORM import ORM_comment, ORM_submission, ORM_subreddit, ORM_subreddit_active_users, ORM_class
from .reddit_parser import Extended_Reddit_RO

@shared_task
def parse_submissions(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)

    subs = client.parse_submission_list(job_id, parse_parameters['submission_url'], parse_parameters['comment_replace_limit'], 
                                        parse_parameters['comment_replace_threshold'])

    for sub, coms in subs:
        atomic_data = [sub] + list(coms)
        save_orm.delay(encode(atomic_data))

@shared_task
def parse_subreddits(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)
    
    subreddits = client.parse_subreddit_list(job_id, parse_parameters['subreddit_name'], parse_parameters['subreddit_query'], 
                                  parse_parameters['subreddit_sort'], parse_parameters['time_filter'], 
                                  parse_parameters['search_limit'], parse_parameters['comment_replace_limit'], parse_parameters['comment_replace_threshold'])
    
    for subreddit in subreddits:
        for submission, coms in subreddit:
            atomic_data = [submission] + list(coms)
            save_orm.delay(encode(atomic_data))

@shared_task
def parse_users(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)

    subreddits = client.parse_subreddits_for_users(job_id, parse_parameters['multi_subreddit_name'], parse_parameters['subreddit_sort_exclusive'], 
                                      parse_parameters['search_limit'], parse_parameters['comment_replace_limit'], 
                                      parse_parameters['comment_replace_threshold'])
    
    for sub, users_list in subreddits:
        atomic_data = [sub]
        for users in users_list:
            atomic_data += users

        save_orm.delay(encode(atomic_data))

@shared_task
def save_orm(entities: str) -> None:

    entity_list = decode(entities)
    for e in entity_list:
        e.write_to_MySQL(NATIVE_SQL_DATABASES['parser'])