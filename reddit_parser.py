from omegaconf import DictConfig
from ORM import ORM_submission, ORM_comment
import hydra
from praw import Reddit
import praw.reddit

class Extended_Reddit_RO(Reddit):

    def __init__(self, client_id: str, client_secret: str, user_agent: str, username: str | None = None, password: str | None = None):

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

    def parse_subreddit(self, subreddit_display_name: str, query: str, sort: str = "new", time_filter: str = "all", limit: int = 10000) -> None:
        
        f = open("subs.txt", "w")
        for submission in self.subreddit(subreddit_display_name).search(query = query, sort = sort, time_filter = time_filter, limit = limit):
            f.write(submission.title)
            f.write("\n")

        f.close()

    def parse_submission(self, submission: str | praw.reddit.Submission) -> dict:
        
        if isinstance(submission, str):
            submission = self.submission(url = submission)
        elif not isinstance(submission, praw.reddit.Submission):
            raise AttributeError("submission must be str (assumed url) or praw.reddit.Submission")

        comments = submission.comments.list()

        return comments

        

@hydra.main(version_base = None, config_path = "conf", config_name = "conf.yaml")
def main(cfg : DictConfig) -> None:

    reddit = Extended_Reddit_RO(
        client_id = cfg.client.reddit_instance.client_id,
        client_secret = cfg.client.reddit_instance.client_secret,
        user_agent = cfg.client.reddit_instance.user_agent,
        username = cfg.user.username,
        password = cfg.user.password,
    )

    if (cfg.mock.get("subreddit_query")):

        reddit.parse_subreddit(
            subreddit_display_name = cfg.mock.subreddit_query.subreddit_display_name,
            query = cfg.mock.subreddit_query.query
        )
    
    if (cfg.mock.get("submission_query")):

        reddit.parse_submission(cfg.mock.submission_query.url)


if __name__ == "__main__":
    main()