import unittest
import os
import tempfile
from faker import Faker
from parameterized import parameterized
from SoftwareTesting.tools import (
    get_java_files,
    read_and_decode_file,
    count_lines,
    count_code_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    calculate_comment_deviation,
    remove_comments,
)

from SoftwareTesting.config import (
    FUNCTIONS,
    CODE_LINES,
    JAVADOC_LINES,
    OTHER_COMMENTS,
)

class TestTools(unittest.TestCase):

    def test_get_java_files(self):
        # Create a temporary directory with dummy .java files
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create dummy .java files
            for i in range(5):
                open(os.path.join(tmpdirname, f"test_file_{i}.java"), "a").close()

            # Retrieve the list of java files
            java_files = get_java_files(tmpdirname)

            # Check if all the files were retrieved
            self.assertEqual(len(java_files), 5)
            # Check if each file actually ends with .java
            for file in java_files:
                self.assertTrue(file.endswith(".java"))

    def test_read_and_decode_file(self):
        fake = Faker()
        # Create a temporary .java file with dummy content
        with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as tmpfile:
            dummy_content = fake.text()
            tmpfile.write(dummy_content.encode("utf-8"))
            tmpfile_path = tmpfile.name

        # Read and decode the temporary file
        decoded_content = read_and_decode_file(tmpfile_path)

        # Check if the decoded content matches the original content
        self.assertEqual(decoded_content, dummy_content)

    def test_count_lines(self):
        fake = Faker()
        # Generate dummy content with random number of lines
        num_lines = fake.random_int(min=1, max=1000)
        dummy_content = "\n".join([fake.word() for _ in range(num_lines)])

        # Count lines in the dummy content
        line_count = count_lines(dummy_content)

        # Check if the counted lines match the number of lines generated
        self.assertEqual(line_count, num_lines)

    def test_remove_comments(self):
        fake = Faker()
        # Generate dummy Java content with comments
        dummy_content_with_comments = fake.text()
        # Remove comments from the dummy content
        content_without_comments = remove_comments(dummy_content_with_comments)

        # Check if the resulting content doesn't contain any comments
        self.assertFalse("/*" in content_without_comments)
        self.assertFalse("//" in content_without_comments)

    def test_count_functions(self):
        fake = Faker()
        # Generate dummy Java content with function declarations
        dummy_content_with_functions = "\n".join(
            ["public void " + fake.word() + "() {" for _ in range(5)]
        )

        # Count functions
        function_count = count_functions(dummy_content_with_functions)

        # Check if the counted functions match the expected number of functions
        self.assertEqual(function_count, 5)

    def test_calculate_comment_deviation(self):
        # Generate a sample metrics dictionary
        metrics = {
            FUNCTIONS: 5,
            CODE_LINES: 100,
            JAVADOC_LINES: 3,
            OTHER_COMMENTS: 5,
        }

        # Calculate comment deviation
        deviation = calculate_comment_deviation(metrics)

        # Check if the calculated deviation matches the expected value
        self.assertAlmostEqual(deviation, -78.66, delta=0.01)

    def test_count_code_lines(self):
        fake = Faker()
        # Generate dummy Java content with code lines
        dummy_content_with_code = "\n".join([fake.word() for _ in range(10)])
        # Add some empty lines and comments to the content
        dummy_content_with_code_and_comments = (
            dummy_content_with_code
            + "\n"
            + "// This is a comment\n\n/* This is a multi-line\n comment */\n"
        )

        # Count lines of code
        code_line_count = count_code_lines(dummy_content_with_code_and_comments)

        # Check if the counted lines match the expected number of code lines
        self.assertEqual(code_line_count, 13)

    def test_count_comments(self):
        fake = Faker()
        # Generate dummy Java content with comments
        dummy_content_with_comments = (
            "\n".join(["// This is a comment" for _ in range(5)])
            + "\n"
            + f"/* This is a multi-line\n comment {fake.text()} */\n"
        )

        # Count lines of comments
        comment_line_count = count_comments(dummy_content_with_comments)

        # Check if the counted lines match the expected number of comment lines
        self.assertEqual(comment_line_count, 6)

    def test_count_javadoc_comments(self):
        fake = Faker()
        # Generate dummy Java content with Javadoc comments
        dummy_content_with_javadoc_comments = "\n".join(
            [f"/** This is a Javadoc comment {{fake.text()}} */" for _ in range(5)]
        )

        # Count lines of Javadoc comments
        javadoc_comment_line_count = count_javadoc_comments(
            dummy_content_with_javadoc_comments
        )

        # Check if the counted lines match the expected number of Javadoc comment lines
        self.assertEqual(javadoc_comment_line_count, 5)

    ####################################### PARAMETERIZED #################################

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
            (5,),
            (10,),
            (15,),
        ]
    )
    def test_count_comments(self, num_comments):
        fake = Faker()
        # Generate dummy Java content with comments
        dummy_content_with_comments = (
            "\n".join(["// This is a comment" for _ in range(num_comments)])
            + "\n"
            + f"/* This is a multi-line\n comment {fake.text()} */\n"
        )

        # Count lines of comments
        comment_line_count = count_comments(dummy_content_with_comments)

        # Check if the counted lines match the expected number of comment lines
        self.assertEqual(comment_line_count, num_comments + 1)

    @parameterized.expand(
        [
            (5,),
            (10,),
            (15,),
        ]
    )
    def test_count_javadoc_comments(self, num_javadoc_comments):
        fake = Faker()
        # Generate dummy Java content with Javadoc comments
        dummy_content_with_javadoc_comments = "\n".join(
            [
                f"/** This is a Javadoc comment {fake.text()} */"
                for _ in range(num_javadoc_comments)
            ]
        )

        # Count lines of Javadoc comments
        javadoc_comment_line_count = count_javadoc_comments(
            dummy_content_with_javadoc_comments
        )

        # Check if the counted lines match the expected number of Javadoc comment lines
        self.assertEqual(javadoc_comment_line_count, num_javadoc_comments)


if __name__ == "__main__":
    unittest.main()
