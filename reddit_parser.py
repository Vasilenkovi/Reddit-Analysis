from omegaconf import DictConfig
from ORM import ORM_submission, ORM_comment
import hydra
from praw import Reddit
import praw.reddit
from collections.abc import Generator

class Extended_Reddit_RO(Reddit):
    """Class that encapsulates logic of structural retrieval of public objects through Reddit API"""

    def __init__(self, client_id: str, client_secret: str, user_agent: str, username: str | None = None, password: str | None = None):
        """Parameters:
            client_id - client id of registered Reddit app;\n
            client_secret - client secret of registered Reddit app;\n
            user_agent - unique user agent;\n
            username - provide to access private content of user;\n
            password - provide to access private content of user;\n"""

        if username and password:
            super().__init__(
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent,
                username = username,
                password = password
            )
        else:
            super().__init__(
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent
            )

    def parse_subreddit(self, subreddit_display_name: str, query: str, sort: str = "new", time_filter: str = "all", limit: int = 10000, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> Generator[tuple[ORM_submission, Generator[ORM_comment, None, None]], None, None]:
        """Description: Returns multiple submissions matched with given query through Reddit search. Takes considerable time to execute (approximately 1 second for every 100 submissions + time to replace "more comments"). Reddit API has been known to return not more than a 1000 submissions this way.\n
        Parameters: \n
            subreddit_display_name - visible, case insensitive name of subreddit to search from;\n
            query - string to match in search;\n
            sort - sorting methods (includes "relevance", "hot", "top", "new");\n
            time_filter - method of limiting the search timeframe (includes "all", "day", "hour", "month", "week", or "year");\n
            limit - the maximum number of submissions to retrieve. Reddit API has been known to return not more than 1000 submissions;\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incures a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: A generator of tuples: Submission and generator of Submission's comments.
        """
        
        for submission in self.subreddit(subreddit_display_name).search(query = query, sort = sort, time_filter = time_filter, limit = limit):
            yield self.parse_submission(submission, comment_replace_limit, comment_replace_threshold)

    def parse_submission(self, submission: str | praw.reddit.Submission, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> tuple[ORM_submission, Generator[ORM_comment, None, None]]:
        """Description: Parses specified submission and its comments. Takes considerable time to execute (approximately 1 second + time to replace "more comments").\n
        Parameters: \n
            submission - url or Submission object for compatibility. Both execution paths require 1 network call (approximately 1 second);\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incurs a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: Tuple of Submission and generator of Submission's comments"""
        
        submission_url = submission #assume url was provided

        if isinstance(submission, str):
            submission = self.submission(url = submission) #Network call
        elif isinstance(submission, praw.reddit.Submission):
            submission_url = submission.url #Network call
        else:
            raise AttributeError("submission must be str (assumed url) or praw.reddit.Submission")
        
        submission_name = submission.name
        submission_title = submission.title
        submission_text_body = submission.selftext
        submission_upvotes = submission.ups
        submission_downvotes = submission.downs
        submission_created_timestamp = int(submission.created)
        submission_author = "" #assume deleted author account

        if submission.author: #if author account was not deleted
            submission_author = submission.author_fullname

        submission_instance = ORM_submission(submission_url, submission_name, submission_title, submission_text_body, submission_author, submission_upvotes, submission_downvotes, submission_created_timestamp)
        
        submission.comments.replace_more(limit = comment_replace_limit, threshold = comment_replace_threshold) #incurs network calls ~comment_replace_limit

        def comment_generator() -> Generator[ORM_comment, None, None]:
            """Helper function to create a comment generator"""

            for comment in submission.comments.list():
                full_name = comment.fullname
                text_body = comment.body
                upvotes = comment.ups
                downvotes = comment.downs
                created_timestamp = int(comment.created)
                author = "" #assume deleted author account

                if comment.author: #if author account was not deleted
                    author = comment.author_fullname

                yield ORM_comment(submission_name, full_name, text_body, author, upvotes, downvotes, created_timestamp)

        return submission_instance, comment_generator()
    

def parse_subreddit_to_db(reddit_config: DictConfig, subreddit_config: DictConfig, db_config: DictConfig) -> None:
    """Description: Parses subreddit and writes results to database based on dictionaries.\n
    Keys accessed:\n
        reddit_config.client_id - client id of registered Reddit app;\n
        reddit_config.client_secret - client secret of registered Reddit app;\n
        reddit_config.user_agent - unique user agent;\n
        \n
        subreddit_config.subreddit_display_name - visible, case insensitive name of subreddit to search from;\n
        subreddit_config.query - string to match in search;\n
        subreddit_config.sort - sorting methods (includes "relevance", "hot", "top", "new");\n
        subreddit_config.time_filter - method of limiting the search timeframe (includes "all", "day", "hour", "month", "week", or "year");\n
        subreddit_config.limit - the maximum number of submissions to retrieve. Reddit API has been known to return not more than a 1000 submissions;\n
        subreddit_config.comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incurs a network call (around 1 second of wait time);\n
        subreddit_config.comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        \n
        db_config.user - database user with dml privileges to provided database;\n
        db_config.password - password for provided user;\n
        db_config.database - database with necessary tables;\n
        db_config.host - address for database connection;\n
        db_config.port - port for database connection;\n
        db_config.use_pure - boolean to use pure python connection instead of c implementation. True value recommended;\n
    Returns: None"""
    
    reddit = Extended_Reddit_RO(
        client_id = reddit_config.client_id,
        client_secret = reddit_config.client_secret,
        user_agent = reddit_config.user_agent
    )

    sub_gen = reddit.parse_subreddit(
            subreddit_display_name = subreddit_config.subreddit_display_name,
            query = subreddit_config.query,
            sort = subreddit_config.sort,
            time_filter = subreddit_config.time_filter,
            limit = subreddit_config.limit,
            comment_replace_limit = subreddit_config.comment_replace_limit,
            comment_replace_threshold = subreddit_config.comment_replace_threshold
    )

    for submission, com_gen in sub_gen:
        submission.write_to_MySQL(db_config)

        for com in com_gen:
            com.write_to_MySQL(db_config)

def parse_submission_to_db(reddit_config: DictConfig, submission_config: DictConfig, db_config: DictConfig) -> None:
    """Description: Parses submission and writes results to database based on dictionaries.\n
    Keys accessed:\n
        reddit_config.client_id - client id of registered Reddit app;\n
        reddit_config.client_secret - client secret of registered Reddit app;\n
        reddit_config.user_agent - unique user agent;\n
        \n
        submission_config.url - url of submission. Incurs network call either way;\n
        submission_config.limit - how many "more comments" to replace in each submission. Each replacement incures a network call (around 1 second of wait time);\n,
        submission_config.threshold - comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        \n
        db_config.user - database user with dml priveleges to provided database;\n
        db_config.password - password for provided user;\n
        db_config.database - database with necessary tables;\n
        db_config.host - address for database connection;\n
        db_config.port - port for database connection;\n
        db_config.use_pure - boolean to use pure python connection instead of c implementation. True value recommended;\n
    Returns: None"""
    
    reddit = Extended_Reddit_RO(
        client_id = reddit_config.client_id,
        client_secret = reddit_config.client_secret,
        user_agent = reddit_config.user_agent
    )

    submission, com_gen = reddit.parse_submission(
        submission = submission_config.url,
        comment_replace_limit = submission_config.limit,
        comment_replace_threshold = submission_config.threshold
    )
    
    submission.write_to_MySQL(db_config)

    for com in com_gen:
        com.write_to_MySQL(db_config)

@hydra.main(version_base = None, config_path = "conf", config_name = "conf.yaml")
def main(cfg : DictConfig) -> None:
    """Main for testing and debugging"""

    if (cfg.mock.get("subreddit_query")):
        parse_subreddit_to_db(cfg.client, cfg.mock.subreddit_query, cfg.db)
    
    if (cfg.mock.get("submission_query")):
        parse_submission_to_db(cfg.client, cfg.mock.submission_query, cfg.db)

if __name__ == "__main__":
    main()