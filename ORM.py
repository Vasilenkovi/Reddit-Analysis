
from abc import ABC, abstractmethod
from mysql.connector import Connect
import time

class ORM_class(ABC):
    """Abstract base class for ORM classes.\n
       db_config used throughout methods accesses following keys:
            db_config.user - database user with dml priveleges to provided database;\n
            db_config.password - password for provided user;\n
            db_config.database - database with necessary tables;\n
            db_config.host - address for database connection;\n
            db_config.port - port for database connection;\n
            db_config.use_pure - boolean to use pure python connection instead of c implementation. True value recommended;\n"""
    
    def __init__(self):
        pass

    @abstractmethod
    def write_to_MySQL(self, db_config: dict) -> None:
        """Write object to database."""
        pass

    @abstractmethod
    def test_MySQL(self, db_config: dict) -> bool:
        """Test for object in database by unique indices."""
        pass

class ORM_submission(ORM_class):

    def __init__(self, url: str, full_name: str, title: str, text_body: str, author: str, upvotes: int, downvotes: int, timestamp: int):

        super().__init__()

        assert len(url) < 768, "url must be less than 768 bytes to fit MySQL unique constraint"
        assert len(full_name) < 768, "full_name must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."

        self.url = url
        self.full_name = full_name
        self.title = title
        self.text_body = text_body
        self.author = author
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.timestamp = timestamp
        self.parsed_timestamp = int(time.time())

    def write_to_MySQL(self, db_config: dict) -> None:
        
        if not self.test_MySQL(db_config):
            cnx = Connect(**db_config)
            cur = cnx.cursor()
            cur.reset()

            query = """INSERT INTO reddit_parsing.submission(url, full_name, title, text_body, author, upvotes, downvotes, created_timestamp, parsed_timestamp) 
            VALUES (%(url)s, %(full_name)s, %(title)s, %(text_body)s, %(author)s, %(upvotes)s, %(downvotes)s, FROM_UNIXTIME(%(timestamp)s), FROM_UNIXTIME(%(parsed_timestamp)s))"""

            cur.execute(query, params = {
                'url': self.url,
                'full_name': self.full_name, 
                'title': self.title, 
                'text_body': self.text_body, 
                'author': self.author,
                'upvotes': self.upvotes,
                'downvotes': self.downvotes,
                'timestamp': self.timestamp, 
                'parsed_timestamp': self.parsed_timestamp
            })
            cnx.commit()
            cnx.close()

    def test_MySQL(self, db_config: dict) -> bool:

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """SELECT full_name FROM reddit_parsing.submission 
        WHERE full_name = %(testing_name)s"""
        
        cur.execute(query, {'testing_name': self.full_name})
        result_full_name = cur.fetchall()
        cur.reset()

        query = """SELECT url FROM reddit_parsing.submission 
        WHERE url = %(testing_url)s"""
        
        cur.execute(query, {'testing_url': self.url})
        result_url = cur.fetchall()

        cnx.close()

        return (len(result_full_name) > 0) or (len(result_url) > 0)

class ORM_comment(ORM_class):

    def __init__(self, parent_submission_name: str, full_name: str, text_body: str, author: str, upvotes: int, downvotes: int, timestamp: int):

        super().__init__()

        assert len(parent_submission_name) < 768, "url must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."
        assert len(full_name) < 768, "full_name must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."

        self.parent_submission_name = parent_submission_name
        self.full_name = full_name
        self.text_body = text_body
        self.author = author
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.timestamp = timestamp
        self.parsed_timestamp = int(time.time())

    def write_to_MySQL(self, db_config: dict) -> None:

        if not self.test_MySQL(db_config):

            cnx = Connect(**db_config)
            cur = cnx.cursor()
            cur.reset()

            query = """INSERT INTO reddit_parsing.submission_comment(full_name, submission_name, text_body, author, upvotes, downvotes, created_timestamp, parsed_timestamp) 
            VALUES (%(full_name)s, %(parent_submission_name)s, %(text_body)s, %(author)s, %(upvotes)s, %(downvotes)s, FROM_UNIXTIME(%(timestamp)s), FROM_UNIXTIME(%(parsed_timestamp)s))"""

            cur.execute(query, params = {
                'full_name': self.full_name, 
                'parent_submission_name': self.parent_submission_name,
                'text_body': self.text_body, 
                'author': self.author,
                'upvotes': self.upvotes,
                'downvotes': self.downvotes,
                'timestamp': self.timestamp, 
                'parsed_timestamp': self.parsed_timestamp
            })
            cnx.commit()
            cnx.close()

    def test_MySQL(self, db_config: dict) -> bool:

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """SELECT full_name FROM reddit_parsing.submission_comment 
        WHERE full_name = %(testing_name)s"""
        
        cur.execute(query, {'testing_name': self.full_name})
        result_unique = cur.fetchall()
        cur.reset()

        query = """SELECT full_name FROM reddit_parsing.submission 
        WHERE full_name = %(testing_submission_full_name)s"""

        cur.execute(query, {'testing_submission_full_name': self.parent_submission_name})
        result_foreign = cur.fetchall()
        
        cnx.close()

        return (len(result_unique) > 0) or (len(result_foreign) < 1)
    
class ORM_subreddit(ORM_class):

    def __init__(self, full_name: str, display_name: str, url: str):

        super().__init__()

        assert len(full_name) < 768, "full_name must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."
        assert display_name, "display_name cant be None"
        assert url, "url cant be None"

        self.full_name = full_name
        self.display_name = display_name
        self.url = url
        self.parsed_timestamp = int(time.time())

    def write_to_MySQL(self, db_config: dict) -> None:

        if not self.test_MySQL(db_config):

            cnx = Connect(**db_config)
            cur = cnx.cursor()
            cur.reset()

            query = """INSERT INTO reddit_parsing.subreddit(full_name, display_name, url, parsed_timestamp) 
            VALUES (%(full_name)s, %(display_name)s, %(url)s, FROM_UNIXTIME(%(parsed_timestamp)s))"""

            cur.execute(query, params = {
                'full_name': self.full_name, 
                'display_name': self.display_name,
                'url': self.url,
                'parsed_timestamp': self.parsed_timestamp
            })
            cnx.commit()
            cnx.close()

    def test_MySQL(self, db_config: dict) -> bool:

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """SELECT full_name FROM reddit_parsing.subreddit 
        WHERE full_name = %(testing_name)s"""
        
        cur.execute(query, {'testing_name': self.full_name})
        result = cur.fetchall()
        cnx.close()

        return len(result) > 0

class ORM_subreddit_active_users(ORM_class):

    def __init__(self, subreddit_full_name: str, user_full_name: str):

        super().__init__()

        assert len(subreddit_full_name) < 256, "full_name must be less than 256 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."
        assert len(user_full_name) < 256, "full_name must be less than 256 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."

        self.subreddit_full_name = subreddit_full_name
        self.user_full_name = user_full_name
        self.parsed_timestamp = int(time.time())

    def write_to_MySQL(self, db_config: dict) -> None:

        if not self.test_MySQL(db_config):

            cnx = Connect(**db_config)
            cur = cnx.cursor()
            cur.reset()

            query = """INSERT INTO reddit_parsing.subreddit_active_users(subreddit_full_name, user_full_name, parsed_timestamp) 
            VALUES (%(subreddit_full_name)s, %(user_full_name)s, FROM_UNIXTIME(%(parsed_timestamp)s))"""

            cur.execute(query, params = {
                'subreddit_full_name': self.subreddit_full_name, 
                'user_full_name': self.user_full_name,
                'parsed_timestamp': self.parsed_timestamp
            })
            cnx.commit()
            cnx.close()

    def test_MySQL(self, db_config: dict) -> bool:

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """SELECT subreddit_full_name, user_full_name FROM reddit_parsing.subreddit_active_users 
        WHERE subreddit_full_name = %(testing_subreddit_full_name)s AND user_full_name = %(testing_user_full_name)s"""
        
        cur.execute(query, {
            'testing_subreddit_full_name': self.subreddit_full_name,
            'testing_user_full_name': self.user_full_name
            })
        result_unique = cur.fetchall()
        cur.reset()

        query = """SELECT full_name FROM reddit_parsing.subreddit 
        WHERE full_name = %(testing_subreddit_full_name)s"""

        cur.execute(query, {'testing_subreddit_full_name': self.subreddit_full_name})
        result_foreign = cur.fetchall()
        
        cnx.close()

        return (len(result_unique) > 0) or (len(result_foreign) < 1)