from django.test import TestCase, Client
from django.urls import reverse
from ParserApp.forms import Form_types
from unittest.mock import patch


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_parser_interface_view(self):
        response = self.client.get(reverse('parser:start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parser/interface.html')

    @patch('ParserApp.tasks.parse_submissions.delay')
    def test_parser_intrepret_query_submission(self, mock_parse_submissions):
        form_data = {
            'form_type': Form_types.COMMENT_SUBMISSION.value,
            'submission_url': 'https://www.example.com',
            'search_limit': 50,
            'comment_replace_limit': 10,
            'comment_replace_threshold': 5
        }
        response = self.client.post(reverse('parser:report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parser/report.html')
        self.assertIn('job_id', response.context)
        mock_parse_submissions.assert_called_once()

    @patch('ParserApp.tasks.parse_subreddits.delay')
    def test_parser_intrepret_query_subreddit(self, mock_parse_subreddits):
        form_data = {
            'form_type': Form_types.COMMENT_SUBREDDIT.value,
            'subreddit_name': 'example_subreddit',
            'subreddit_query': 'example_query',
            'subreddit_sort': 'hot',
            'time_filter': 'week',
            'search_limit': 50,
            'comment_replace_limit': 10,
            'comment_replace_threshold': 5
        }
        response = self.client.post(reverse('parser:report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parser/report.html')
        self.assertIn('job_id', response.context)
        mock_parse_subreddits.assert_called_once()

    @patch('ParserApp.tasks.parse_users.delay')
    def test_parser_intrepret_query_users(self, mock_parse_users):
        form_data = {
            'form_type': Form_types.USERS.value,
            'multi_subreddit_name': 'example_subreddit',
            'subreddit_sort_exclusive': 'hot',
            'search_limit': 50,
            'comment_replace_limit': 10,
            'comment_replace_threshold': 5
        }
        response = self.client.post(reverse('parser:report'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parser/report.html')
        self.assertIn('job_id', response.context)
        mock_parse_users.assert_called_once()
    # def test_parser_intrepret_query_invalid_type(self):
    #     form_data = {
    #         'form_type': 'invalid_type',
    #     }
    #     response = self.client.post(reverse('parser:report'), data=form_data)
    #     self.assertEqual(response.status_code, 404)