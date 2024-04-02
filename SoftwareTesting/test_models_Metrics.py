from SoftwareTesting.models import Metrics
import unittest

class TestMetrics(unittest.TestCase):

    def test_set_classname_empty_string(self):
        metrics = Metrics()
        metrics.ClassName = ""
        self.assertEqual(metrics.ClassName, "")

    def test_set_javadoclines_negative(self):
        metrics = Metrics(
            ClassName="TestClass",
            JavaDocLines=-5,
            OtherComments=10,
            CodeLines=50,
            Loc=100,
            FunctionLines=20,
            CommentDeviation=0.5,
        )
        self.assertEqual(metrics.JavaDocLines, -5)

    def test_set_loc_negative(self):
        metrics = Metrics()
        metrics.Loc = -5
        self.assertEqual(metrics.Loc, -5)

    def test_set_function_lines_negative(self):
        metrics = Metrics()
        metrics.FunctionLines = -1
        self.assertEqual(metrics.FunctionLines, -1)

    def test_set_comment_deviation_negative(self):
        metrics = Metrics(
            ClassName="TestClass",
            JavaDocLines=10,
            OtherComments=5,
            CodeLines=100,
            Loc=150,
            FunctionLines=20,
            CommentDeviation=0,
        )
        metrics.CommentDeviation = -1
        self.assertEqual(metrics.CommentDeviation, -1)

    def test_set_comment_deviation_greater_than_100(self):
        metrics = Metrics(
            ClassName="Test",
            JavaDocLines=10,
            OtherComments=20,
            CodeLines=30,
            Loc=40,
            FunctionLines=50,
            CommentDeviation=150,
        )
        self.assertEqual(metrics.CommentDeviation, 150)


if __name__ == "__init__":
    unittest.main()
