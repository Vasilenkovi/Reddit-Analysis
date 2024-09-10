from django.test import SimpleTestCase
from .ORM import ORM_submission, ORM_comment, ORM_subreddit, ORM_subreddit_active_users

# Create your tests here.
class ORM_test(SimpleTestCase):

    def test_orm_validation(self):
        # Test valid instantiation
        submission = ORM_submission(
            url = "https://www.reddit.com/r/chairsunderwater/comments/1bx0zm2/my_university_places_chairs_around_the_campus/",
            full_name = "t3_1bx0zm2",
            title = "My university places chairs around the campus from time to time",
            text_body = "",
            author = "t2_1qzw6qed",
            upvotes = 186,
            downvotes = 0,
            timestamp = 1712347020,
            flair = None,
            job_id = "prsc_65"
        )
        comment = ORM_comment(
            parent_submission_name = "t3_1bx0zm2",
            full_name = "t1_kyan1w4",
            text_body = "Out in the open like that!?",
            author = "t2_2iyvwu3c",
            upvotes = 13,
            downvotes = 0,
            timestamp = 1712365140,
            job_id = "prsc_65"
        )
        subreddit = ORM_subreddit(
            full_name = "t5_116qz7",
            display_name = "attackeyes",
            url = "reddit.com/r/attackeyes/",
            job_id = "prsr_27"
        )
        user = ORM_subreddit_active_users(
            subreddit_full_name = "t5_116qz7",
            user_full_name = "t2_10ot5gya8a",
            job_id = "prsr_27"
        )

        # Invalid objects

        with self.assertRaises(AssertionError):
            submission = ORM_submission(
                url = "https://www.reddit.com/r/chairsunderwater/comments/1bx0zm2/my_university_places_chairs_around_the_campus/"*50,
                full_name = "t3_1bx0zm2",
                title = "My university places chairs around the campus from time to time",
                text_body = "",
                author = "t2_1qzw6qed",
                upvotes = 186,
                downvotes = 0,
                timestamp = 1712347020,
                flair = None,
                job_id = "prsc_65"
            )
        
        with self.assertRaises(AssertionError):
            submission = ORM_submission(
                url = "https://www.reddit.com/r/chairsunderwater/comments/1bx0zm2/my_university_places_chairs_around_the_campus/",
                full_name = "t3_1bx0zm2"*50,
                title = "My university places chairs around the campus from time to time",
                text_body = "",
                author = "t2_1qzw6qed",
                upvotes = 186,
                downvotes = 0,
                timestamp = 1712347020,
                flair = None,
                job_id = "prsc_65"
            )
            
        with self.assertRaises(AssertionError):
            comment = ORM_comment(
                parent_submission_name = "t3_1bx0zm2"*50,
                full_name = "t1_kyan1w4",
                text_body = "Out in the open like that!?",
                author = "t2_2iyvwu3c",
                upvotes = 13,
                downvotes = 0,
                timestamp = 1712365140,
                job_id = "prsc_65"
            )
            
        with self.assertRaises(AssertionError):
            comment = ORM_comment(
                parent_submission_name = "t3_1bx0zm2",
                full_name = "t1_kyan1w4"*50,
                text_body = "Out in the open like that!?",
                author = "t2_2iyvwu3c",
                upvotes = 13,
                downvotes = 0,
                timestamp = 1712365140,
                job_id = "prsc_65"
            )
                        
        with self.assertRaises(AssertionError):
            subreddit = ORM_subreddit(
                full_name = "t5_116qz7"*50,
                display_name = "attackeyes",
                url = "reddit.com/r/attackeyes/",
                job_id = "prsr_27"
            )
                        
        with self.assertRaises(AssertionError):
            subreddit = ORM_subreddit(
                full_name = "t5_116qz7",
                display_name = None,
                url = "reddit.com/r/attackeyes/",
                job_id = "prsr_27"
            )
                        
        with self.assertRaises(AssertionError):
            subreddit = ORM_subreddit(
                full_name = "t5_116qz7",
                display_name = "attackeyes",
                url = None,
                job_id = "prsr_27"
            )
                                    
        with self.assertRaises(AssertionError):
            user = ORM_subreddit_active_users(
                subreddit_full_name = "t5_116qz7"*50,
                user_full_name = "t2_10ot5gya8a",
                job_id = "prsr_27"
            )
                                    
        with self.assertRaises(AssertionError):
            user = ORM_subreddit_active_users(
                subreddit_full_name = "t5_116qz7",
                user_full_name = "t2_10ot5gya8a"*50,
                job_id = "prsr_27"
            )