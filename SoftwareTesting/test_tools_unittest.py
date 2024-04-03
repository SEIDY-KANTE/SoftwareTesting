import unittest
import os
import tempfile
from faker import Faker
from SoftwareTesting.utils.tools import (
    get_java_files,
    read_and_decode_file,
    count_lines,
    count_code_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    calculate_comment_deviation,
    remove_comments,
    remove_javadoc_comments,
)

from SoftwareTesting.utils.config import (
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


    def test_count_comments_single_line(self):
        fake = Faker()
        generated_word = fake.word()
        content = "\n".join([f"// {generated_word}" for _ in range(5)])
        self.assertEqual(count_comments(content), 5)

    def test_count_comments_no_comments(self):
        fake = Faker()
        content = "\n".join([fake.word() for _ in range(5)])
        self.assertEqual(count_comments(content), 0)

    def test_remove_javadoc_comments_single_line(self):
        fake = Faker()
        generated_text = fake.text()
        content = (
            "public class Test {\n/** Javadoc comment */"
            + "\npublic void test() {"
            + generated_text
            + "}\n}"
        )
        expected_result = (
            "public class Test {\n" + "\npublic void test() {" + generated_text + "}\n}"
        )
        self.assertEqual(remove_javadoc_comments(content), expected_result)

    def test_remove_javadoc_comments_multi_line(self):
        fake = Faker()
        generated_text = fake.text()
        content = (
            "public class Test {\n/**\n * Multi-line\n * Javadoc comment\n */"
            + "\npublic void test() {"
            + generated_text
            + "}\n}"
        )
        expected_result = (
            "public class Test {\n" + "\npublic void test() {" + generated_text + "}\n}"
        )
        self.assertEqual(remove_javadoc_comments(content), expected_result)

    def test_remove_javadoc_comments_no_comments(self):
        fake = Faker()
        content = (
            "public class Test {" + "\npublic void test() {" + fake.text() + "}\n}"
        )
        self.assertEqual(remove_javadoc_comments(content), content)

    def test_count_javadoc_comments_single_line(self):
        content = "/**\n*Javadoc comment \n*/"
        self.assertEqual(count_javadoc_comments(content), 1)

    def test_count_javadoc_comments_multi_line(self):
        content = "/**\n * Multi-line\n * Javadoc comment\n */"
        self.assertEqual(count_javadoc_comments(content), 2)

    def test_count_javadoc_comments_no_comments(self):
        content = "public class Test {\npublic void test() {}\n}"
        self.assertEqual(count_javadoc_comments(content), 0)


if __name__ == "__main__":
    unittest.main()