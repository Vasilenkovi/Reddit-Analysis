from unittest import TestCase
from mysql import connector
from IdApp.task_id_manager import get_task_id, Job_types, Valid_tables
from DjangoRed.settings import NATIVE_SQL_DATABASES

# Create your tests here.
class Test_job_id_integration(TestCase):

    def setUp(self) -> None:
        self.cnx = connector.connect(**NATIVE_SQL_DATABASES["job_id"])
        self.cur = self.cnx.cursor()
        self.cur.reset()

        self.mock = [
            (Job_types.PARSE_COMMENTS, {"test": "must be deleted"}, Valid_tables.PARSING_COMMENT_ID),
            (Job_types.PARSE_SUBREDDITS, {"test": "must be deleted"}, Valid_tables.PARSING_SUBREDDITS_ID),
            (Job_types.CLUSTER, {"test": "must be deleted"}, Valid_tables.CLUSTERING_ID),
            (Job_types.STAT, {"test": "must be deleted"}, Valid_tables.STATISTICS_SUBREDDITS_ID)
        ]
        self.result = []
    
    def test_job_id(self) -> None:
        for j, d, t in self.mock:
            latest = get_task_id(j, d)
            self.result.append(latest)

            self.cur.reset()
            query = f"SELECT task_id FROM {t} WHERE task_id = '{latest}'"
            self.cur.execute(query)
            res = self.cur.fetchall()[0][0]

            self.assertEqual(res, latest)

            self.cur.reset()
            query = f"DELETE FROM {t} WHERE task_id = '{latest}'"
            self.cur.execute(query)
            self.cur.fetchall()
            self.cnx.commit()

    def test_imports(self) -> None:
        import sys

        import AccountsApp
        self.assertIn("AccountsApp", sys.modules)

        import DatasetViewApp
        self.assertIn("DatasetViewApp", sys.modules)

        import DjangoRed
        self.assertIn("DjangoRed", sys.modules)

        import GraphApp
        self.assertIn("GraphApp", sys.modules)

        import IdApp
        self.assertIn("IdApp", sys.modules)

        import ParserApp
        self.assertIn("ParserApp", sys.modules)

        import StatApp
        self.assertIn("StatApp", sys.modules)

        import VisualizationApp
        self.assertIn("VisualizationApp", sys.modules)

        import WebRedApp
        self.assertIn("WebRedApp", sys.modules)

    def tearDown(self) -> None:
        self.cur.close()
        self.cnx.close()