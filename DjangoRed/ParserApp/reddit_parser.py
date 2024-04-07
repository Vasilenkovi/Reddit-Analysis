from .ORM import ORM_submission, ORM_comment, ORM_subreddit, ORM_subreddit_active_users
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

    def parse_subreddit(self, job_id: str, subreddit_display_name: str, query: str, sort: str = "new", time_filter: str = "all", limit: int = 10000, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> Generator[tuple[ORM_submission, Generator[ORM_comment, None, None]], None, None]:
        """Description: Returns multiple submissions matched with given query through Reddit search. Takes considerable time to execute (approximately 1 second for every 100 submissions + time to replace "more comments"). Reddit API has been known to return not more than a 1000 submissions this way.\n
        Parameters: \n
            subreddit_display_name - visible, case insensitive name of subreddit to search from;\n
            query - string to match in search. If Falsey, subreddit streams will be used according to "sort" attribute;\n
            sort - sorting methods (includes "relevance", "hot", "top", "new");\n
            time_filter - method of limiting the search timeframe (includes "all", "day", "hour", "month", "week", or "year");\n
            limit - the maximum number of submissions to retrieve. Reddit API has been known to return not more than 1000 submissions;\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incures a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: A generator of tuples: Submission and generator of Submission's comments.
        """
        if query:
            for submission in self.subreddit(subreddit_display_name).search(query = query, sort = sort, time_filter = time_filter, limit = limit):
                yield self.parse_submission(job_id, submission, comment_replace_limit, comment_replace_threshold)
        else:
            match sort:
                case "hot":
                    for submission in self.hot(limit = limit):
                        yield self.parse_submission(job_id, submission, comment_replace_limit, comment_replace_threshold)
                case "new":
                    for submission in self.new(limit = limit):
                        yield self.parse_submission(job_id, submission, comment_replace_limit, comment_replace_threshold)
                case "top":
                    for submission in self.top(time_filter = time_filter, limit = limit):
                        yield self.parse_submission(job_id, submission, comment_replace_limit, comment_replace_threshold)
                case _:
                    for submission in self.top(time_filter = "all", limit = limit):
                        yield self.parse_submission(job_id, submission, comment_replace_limit, comment_replace_threshold)


    def parse_submission(self, job_id: str, submission: str | praw.reddit.Submission, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> tuple[ORM_submission, Generator[ORM_comment, None, None]]:
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
            submission_url = "reddit.com" + submission.permalink #Network call
        else:
            raise ValueError("submission must be str (assumed url) or praw.reddit.Submission")
        
        submission_name = submission.name
        submission_title = submission.title
        submission_text_body = submission.selftext
        submission_upvotes = submission.ups
        submission_downvotes = submission.downs
        submission_created_timestamp = int(submission.created)
        submission_author = "" #assume deleted author account
        submission_flair = submission.link_flair_text

        if submission.author: #if author account was not deleted
            submission_author = submission.author_fullname

        submission_instance = ORM_submission(submission_url, submission_name, submission_title, 
                                             submission_text_body, submission_author, submission_upvotes, 
                                             submission_downvotes, submission_created_timestamp, submission_flair,
                                             job_id)
        
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

                yield ORM_comment(submission_name, full_name, text_body, 
                                  author, upvotes, downvotes, 
                                  created_timestamp, job_id)

        return submission_instance, comment_generator()

    def parse_submission_list(self, job_id: str, submissions: list[str], comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> Generator[tuple[ORM_submission, Generator[ORM_comment, None, None]], None, None]:
        """Description: Parses specified submissions and their comments. Takes considerable time to execute (approximately 1 second + time to replace "more comments").\n
        Parameters: \n
            submissions - list of urls. Each item is processed in approximately 1 second;\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incurs a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: Tuple of Submission and generator of Submission's comments"""

        for sub in submissions:
           yield self.parse_submission(job_id, sub, comment_replace_limit, comment_replace_threshold)
    
    def parse_subreddit_users(self, job_id: str, subreddit_display_name: str, sort_discipline: str = "hot", limit: int = 1000, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> tuple[ORM_subreddit, Generator[list[ORM_subreddit_active_users], None, None]]:
        """Description: Parses active users of specified subreddit. Users are selected among posters and commentors. Active users are defined by sort_discipline. Submissions from deleted accounts are dropped. Method uses 1 network call for every 100 submissions (~1 sec for 100 submissions) + network call for every comment replacement.\n
        Parameters: \n
            subreddit_display_name - visible, case insensitive name of subreddit to search from;\n
            sort_discipline - how active users are defined. Options: "hot", "new", "top". Coerces hot otherwise. Top is limited by month;\n
            limit - the maximum number of submissions to retrieve. Reddit API has been known to return not more than 1000 submissions;\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incurs a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: Tuple of Subreddit and generator of Subreddit's active users grouped by submissions"""

        subreddit = self.subreddit(subreddit_display_name)
        full_url = "reddit.com" + subreddit.url
        sub_orm = ORM_subreddit(subreddit.fullname, subreddit_display_name, full_url, job_id)

        submission_generator = None
        match sort_discipline:
            case "hot":
                submission_generator = subreddit.hot(limit = limit)
            case "new":
                submission_generator = subreddit.new(limit = limit)
            case "top":
                submission_generator = subreddit.top(time_filter = "month", limit = limit)
            case _:
                submission_generator = subreddit.hot(limit = limit)

        def author_generator() -> Generator[ORM_subreddit_active_users, None, None]:
            """Helper function to create a comment author generator"""

            for submission in submission_generator:
                total_user_list = []

                if submission.author: #Submissions from deleted accounts set this field to None
                    total_user_list.append(ORM_subreddit_active_users(subreddit.fullname, submission.author_fullname, job_id))

                submission.comments.replace_more(limit = comment_replace_limit, threshold = comment_replace_threshold)

                for comment in submission.comments.list():
                    if comment.author: #Comments from deleted accounts set this field to None
                        total_user_list.append(ORM_subreddit_active_users(subreddit.fullname, comment.author_fullname, job_id))

                yield total_user_list

        return sub_orm, author_generator()
    
    def parse_subreddits_for_users(self, job_id: str, subreddits: list, sort_discipline: str = "hot", limit: int = 1000, comment_replace_limit: int | None = 0, comment_replace_threshold: int = 1) -> Generator[tuple[ORM_subreddit, Generator[list[ORM_subreddit_active_users], None, None]], None, None]:
        """Description: Parses active users of specified subreddits. Users are selected among posters and commentors. Active users are defined by sort_discipline. Submissions from deleted accounts are dropped. Method uses 1 network call for every 100 submissions (~1 sec for 100 submissions) + network call for every comment replacement.\n
        Parameters: \n
            subreddits - list of visible, case insensitive names of subreddits to search from;\n
            sort_discipline - how active users are defined. Options: "hot", "new", "top". Coerces hot otherwise;\n
            limit - the maximum number of submissions to retrieve. Reddit API has been known to return not more than 1000 submissions;\n
            comment_replace_limit - how many "more comments" to replace in each submission. Each replacement incurs a network call (around 1 second of wait time);\n
            comment_replace_threshold - how many additional replies "more comments" must have to incur a replacement call;\n
        Returns: Tuple of Subreddit and generator of Subreddit's active users grouped by submissions"""
                
        for sub in subreddits:
            yield self.parse_subreddit_users(job_id, sub, sort_discipline, limit, comment_replace_limit, comment_replace_threshold)