
from abc import ABC, abstractmethod
from mysql.connector import Connect
import time

class ORM_class(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def write_to_MySQL(self, db_config: dict) -> None:
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

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """INSERT INTO reddit_parsing.submission(url, full_name, title, text_body, author, upvotes, downvotes, created_timestamp, parsed_timestamp) 
        VALUES ('{url}', '{full_name}', '{title}', '{text_body}', '{author}', {upvote}, {downvotes}, FROM_UNIXTIME({timestamp}), FROM_UNIXTIME({parsed_timestamp}))""".format(
            url = self.url, full_name = self.full_name, title = self.title, text_body = self.text_body, author = self.author,
            upvote = self.upvotes, downvotes = self.downvotes, timestamp = self.timestamp, parsed_timestamp = self.parsed_timestamp
        )

        cur.execute(query)
        cnx.commit()
        cnx.close()

class ORM_comment(ORM_class):

    def __init__(self, parent_submission_name: str, full_name: str, title: str, text_body: str, author: str, upvotes: int, downvotes: int, timestamp: int):

        super().__init__()

        assert len(parent_submission_name) < 768, "url must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."
        assert len(full_name) < 768, "full_name must be less than 768 bytes to fit MySQL unique constraint. Since Reddit enforces limit on full_name length, I will be surprised to find you here."

        self.parent_submission_name = parent_submission_name
        self.full_name = full_name
        self.title = title
        self.text_body = text_body
        self.author = author
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.timestamp = timestamp
        self.parsed_timestamp = int(time.time())

    def write_to_MySQL(self, db_config: dict) -> None:

        cnx = Connect(**db_config)
        cur = cnx.cursor()
        cur.reset()

        query = """INSERT INTO reddit_parsing.submission_comment(full_name, submission_name, title, text_body, author, upvotes, downvotes, created_timestamp, parsed_timestamp) 
        VALUES ('{full_name}', '{parent_submission_name}', '{title}', '{text_body}', '{author}', {upvote}, {downvotes}, FROM_UNIXTIME({timestamp}), FROM_UNIXTIME({parsed_timestamp}))""".format(
            full_name = self.full_name, parent_submission_name = self.parent_submission_name, title = self.title, text_body = self.text_body,
            author = self.author, upvote = self.upvotes, downvotes = self.downvotes, timestamp = self.timestamp, parsed_timestamp = self.parsed_timestamp
        )

        cur.execute(query)
        cnx.commit()
        cnx.close()