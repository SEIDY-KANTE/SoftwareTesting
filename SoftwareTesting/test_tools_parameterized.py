import unittest
import os
import tempfile
from faker import Faker
from parameterized import parameterized
from SoftwareTesting.tools import (
    get_java_files,
    count_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    calculate_comment_deviation,
    remove_comments,
    remove_javadoc_comments,
)

from SoftwareTesting.config import (
    FUNCTIONS,
    CODE_LINES,
    JAVADOC_LINES,
    OTHER_COMMENTS,
)


class TestToolsParameterized(unittest.TestCase):

    @parameterized.expand(
        [
            (0, 0),
            (10, 10),
            (15, 15),
        ]
    )
    def test_get_java_files(self, num_files, expected_count):
        # Create a temporary directory with dummy .java files
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create dummy .java files
            for i in range(num_files):
                open(os.path.join(tmpdirname, f"test_file_{i}.java"), "a").close()

            # Retrieve the list of java files
            java_files = get_java_files(tmpdirname)

            # Check if all the files were retrieved
            self.assertEqual(len(java_files), expected_count)
            # Check if each file actually ends with .java
            for file in java_files:
                self.assertTrue(file.endswith(".java"))

    @parameterized.expand(
        [
            (5, 5),
            (10, 10),
            (15, 15),
        ]
    )
    def test_count_lines(self, num_lines, expected_count):
        fake = Faker()
        # Generate dummy content with specified number of lines
        dummy_content = "\n".join([fake.word() for _ in range(num_lines)])

        # Count lines in the dummy content
        line_count = count_lines(dummy_content)

        # Check if the counted lines match the expected number of lines
        self.assertEqual(line_count, expected_count)

    @parameterized.expand(
        [
            (5,),
            (10,),
            (15,),
        ]
    )
    def test_count_functions(self, num_functions):
        fake = Faker()
        # Generate dummy Java content with function declarations
        dummy_content_with_functions = "\n".join(
            ["public void " + fake.word() + "() {" for _ in range(num_functions)]
        )

        # Count functions
        function_count = count_functions(dummy_content_with_functions)

        # Check if the counted functions match the expected number of functions
        self.assertEqual(function_count, num_functions)

    @parameterized.expand(
        [
            ("No_Function", "", 0),
            ("One_Function", "public void testFunction() {}", 1),
            (
                "Multiple_Functions",
                "public void func1() {}\nprivate int func2() {\nreturn 0;\n}",
                2,
            ),
        ]
    )
    def test_count_functions(self, name, content, expected_count):
        function_count = count_functions(content)
        self.assertEqual(function_count, expected_count)

    @parameterized.expand(
        [
            (
                "No_Functions",
                {
                    FUNCTIONS: 0,
                    CODE_LINES: 100,
                    JAVADOC_LINES: 20,
                    OTHER_COMMENTS: 10,
                },
                0.0,
            ),
            (
                "Sample_Metrics",
                {
                    FUNCTIONS: 5,
                    CODE_LINES: 100,
                    JAVADOC_LINES: 20,
                    OTHER_COMMENTS: 10,
                },
                -20.0,
            ),
            (
                "Zero_Code_Lines",
                {
                    FUNCTIONS: 0,
                    CODE_LINES: 0,
                    JAVADOC_LINES: 0,
                    OTHER_COMMENTS: 0,
                },
                0.0,
            ),
        ]
    )
    def test_calculate_comment_deviation(self, name, metrics, expected_deviation):
        deviation = calculate_comment_deviation(metrics)
        self.assertAlmostEqual(deviation, expected_deviation)

    @parameterized.expand(
        [
            (5, ["// comment" for _ in range(5)]),
            (0, [Faker().word() for _ in range(5)]),
        ]
    )
    def test_count_comments(self, expected_count, content):
        content = "\n".join(content)
        self.assertEqual(count_comments(content), expected_count)

    @parameterized.expand(
        [
            (["// test"], "// test"),
            (["/** Javadoc comment */", "// test"], "\n// test"),
        ]
    )
    def test_remove_javadoc_comments(self, content_lines, expected_result):
        content = "\n".join(content_lines)
        self.assertEqual(remove_javadoc_comments(content), expected_result)

    @parameterized.expand(
        [
            (["// test"], ""),
            (["/*\n *Multiline comments\n */"], ""),
            (["/** Javadoc comment */", "// test1"], "\n"),
            (["/*\n *Multiline comments\n */", "// test1"], "\n"),
            (
                ["/*\n *Multiline comments 1\n *Multiline comments 2\n */", "// test3"],
                "\n",
            ),
        ]
    )
    def test_remove_comments(self, content_lines, expected_result):
        content = "\n".join(content_lines)
        self.assertEqual(remove_comments(content), expected_result)

    @parameterized.expand(
        [
            (1, "/**\n *Javadoc comment \n*/"),
            (2, "/**\n * Multi-line\n * Javadoc comment\n */"),
            (0, "public class Test {\npublic void test() {}\n}"),
        ]
    )
    def test_count_javadoc_comments(self, expected_count, content):
        self.assertEqual(count_javadoc_comments(content), expected_count)


if __name__ == "__main__":
    unittest.main()
