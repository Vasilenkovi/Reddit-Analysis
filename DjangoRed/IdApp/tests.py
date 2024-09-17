from django.test import SimpleTestCase
from .db_query import _select_in_limit_query

class Db_query_build_test(SimpleTestCase):

    def test_in_limit_query(self):
        # Normal query
        query = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
        params = {}
        in_params = ["prsr_27", "prsr_28", "prsr_29"]
        limit = 1000
        offset = 1000

        expected = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id IN ( %(prsr_27)s, %(prsr_28)s, %(prsr_29)s )
                    LIMIT 1000 OFFSET 1000;"""
        expected_params = {
            "prsr_27": "prsr_27",
            "prsr_28": "prsr_28",
            "prsr_29": "prsr_29"
        }

        result = _select_in_limit_query(query, params, in_params, limit, offset)
        self.assertEqual(expected, result)
        self.assertEqual(expected_params, params)
        
        # Single parameter
        query = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
        params = {}
        in_params = ["prsr_27"]
        limit = 1000
        offset = 1000

        expected = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id IN ( %(prsr_27)s )
                    LIMIT 1000 OFFSET 1000;"""
        expected_params = {
            "prsr_27": "prsr_27"
        }

        result = _select_in_limit_query(query, params, in_params, limit, offset)
        self.assertEqual(expected, result)
        self.assertEqual(expected_params, params)

        # Missing limit and offset parameters
        query = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
        params = {}
        in_params = ["prsr_27"]

        expected = """SELECT su.job_id, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id IN ( %(prsr_27)s )
                    LIMIT 1000 OFFSET 0;"""
        expected_params = {
            "prsr_27": "prsr_27"
        }

        result = _select_in_limit_query(query, params, in_params)
        self.assertEqual(expected, result)
        self.assertEqual(expected_params, params)

        # Non-empty params
        query = """SELECT %(column)s, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
        params = {"column": "su.job_id"}
        in_params = ["prsr_27"]

        expected = """SELECT %(column)s, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id IN ( %(prsr_27)s )
                    LIMIT 1000 OFFSET 0;"""
        expected_params = {
            "column": "su.job_id",
            "prsr_27": "prsr_27"
        }

        result = _select_in_limit_query(query, params, in_params)
        self.assertEqual(expected, result)
        self.assertEqual(expected_params, params)
        
        # Funny SQL injection
        query = """SELECT %(column)s, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id {in_expr}
                    LIMIT {limit} OFFSET {offset};"""
        params = {"column": "su.job_id"}
        in_params = ["';SELECT * FROM information_schema.tables;--"]

        expected = """SELECT %(column)s, su.user_full_name, su.subreddit_full_name, su.parsed_timestamp, s.display_name, s.url
                    FROM reddit_parsing.subreddit_active_users AS su 
                    JOIN reddit_parsing.subreddit AS s ON (su.job_id = s.job_id) AND (su.subreddit_full_name = s.full_name)
                    WHERE su.job_id IN ( %(';SELECT * FROM information_schema.tables;--)s )
                    LIMIT 1000 OFFSET 0;"""
        expected_params = {
            "column": "su.job_id",
            "';SELECT * FROM information_schema.tables;--": "';SELECT * FROM information_schema.tables;--"
        }

        result = _select_in_limit_query(query, params, in_params)
        self.assertEqual(expected, result)
        self.assertEqual(expected_params, params)