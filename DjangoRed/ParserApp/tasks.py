import ORM
from reddit_parser import Extended_Reddit_RO
from DjangoRed.settings import NATIVE_SQL_DATABASES, REDDIT_CLIENT
from celery import shared_task

@shared_task
def parse_submission(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)

    sub, coms = client.parse_submission(job_id, parse_parameters['submission'], parse_parameters['comment_replace_limit'], 
                                        parse_parameters['comment_replace_threshold'])

    atomic_data = [sub] + list(coms)
    save.delay(atomic_data)

@shared_task
def parse_subreddit(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)
    
    subs = client.parse_subreddit(job_id, parse_parameters['subreddit_display_name'], parse_parameters['query'], parse_parameters['sort'],
                           parse_parameters['time_filter'], parse_parameters['limit'], parse_parameters['comment_replace_limit'],
                           parse_parameters['comment_replace_threshold'])
    
    for sub, coms in subs:
        atomic_data = [sub] + list(coms)
        save.delay(atomic_data)

@shared_task
def parse_users(job_id: str, parse_parameters: dict) -> None:
    client = Extended_Reddit_RO(REDDIT_CLIENT.client_id, REDDIT_CLIENT.client_secret, REDDIT_CLIENT.user_agent)

    subreddits = client.parse_subreddits_for_users(job_id, parse_parameters['subreddits'], parse_parameters['sort_discipline'], 
                                      parse_parameters['limit'], parse_parameters['comment_replace_limit'], 
                                      parse_parameters['comment_replace_threshold'])
    
    for sub, users in subreddits:
        atomic_data = [sub] + list(users)
        save.delay(atomic_data)

@shared_task
def save(entity_list: list[ORM.ORM_class]) -> None:
    for e in entity_list:
        e.write_to_MySQL(NATIVE_SQL_DATABASES['parser'])