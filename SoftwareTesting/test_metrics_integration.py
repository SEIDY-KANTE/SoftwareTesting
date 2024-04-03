from django.test import TestCase
from SoftwareTesting.models.models import Metrics
import unittest

class TestMetricsIntegration(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create sample metrics in the test database
        Metrics.objects.create(
            ClassName="JavaFile.java",
            JavaDocLines=10,
            OtherComments=5,
            CodeLines=100,
            Loc=150,
            FunctionLines=20,
            CommentDeviation=0,
        )

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database after all tests are done
        Metrics.objects.all().delete()

    def test_get_metrics_from_database(self):
        # Query metrics from the database
        metrics = Metrics.objects.all()

        # Assert that metrics are retrieved
        self.assertEqual(len(metrics), 1)

        # Check the attributes of the retrieved metrics
        metric = metrics[0]
        self.assertEqual(metric.ClassName, "JavaFile.java")
        self.assertEqual(metric.JavaDocLines, 10)
        self.assertEqual(metric.OtherComments, 5)
        self.assertEqual(metric.CodeLines, 100)
        self.assertEqual(metric.Loc, 150)
        self.assertEqual(metric.FunctionLines, 20)
        self.assertEqual(metric.CommentDeviation, 0)

    def test_update_metrics_in_database(self):
        # Retrieve metrics from the database
        metric = Metrics.objects.get(ClassName="JavaFile.java")

        # Update some attribute
        metric.JavaDocLines = 20
        metric.save()

        # Retrieve the updated metric from the database
        updated_metric = Metrics.objects.get(ClassName="JavaFile.java")

        # Assert that the attribute has been updated
        self.assertEqual(updated_metric.JavaDocLines, 20)

    def test_delete_metrics_from_database(self):
        # Delete metrics from the database
        Metrics.objects.filter(ClassName="JavaFile.java").delete()

        # Query metrics from the database
        metrics = Metrics.objects.all()

        # Assert that no metrics are retrieved
        self.assertEqual(len(metrics), 0)


if __name__ == "__init__":
    unittest.main()
