"""
These integration tests simulate real-world scenarios by creating temporary files with dummy Java content. 
They ensure that the functions interact correctly with these files and produce the expected results.
"""

import unittest
import os
import tempfile
from SoftwareTesting.tools import (
    get_java_files,
    read_and_decode_file,
    count_lines,
    remove_comments,
    count_code_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    calculate_comment_deviation,
)
from SoftwareTesting.config import (
    FUNCTIONS,
    CODE_LINES,
    JAVADOC_LINES,
    OTHER_COMMENTS,
)

class TestToolsIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_files = [
            "TestFile1.java",
            "TestFile2.java",
            "TestFile3.java",
        ]
        self.test_contents = [
            "public class TestFile1 {\n// This is a comment\n}",
            "public class TestFile2 {\n/* This is a\nmulti-line comment */\n}",
            "public class TestFile3 {\n/* This is a Javadoc comment */\n}",
        ]

        # Create temporary Java files with dummy content
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            with open(file_path, "w") as file:
                file.write(content)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_java_files(self):
        # Retrieve Java files from the temporary directory
        java_files = get_java_files(self.temp_dir.name)

        # Check if all the files were retrieved
        self.assertEqual(len(java_files), len(self.test_files))
        # Check if each file actually ends with .java
        for file in java_files:
            self.assertTrue(file.endswith(".java"))

    # def test_read_and_decode_file(self):
    #     for file_name, content in zip(self.test_files, self.test_contents):
    #         file_path = os.path.join(self.temp_dir.name, file_name)
    #         # Read and decode each temporary file
    #         decoded_content = read_and_decode_file(file_path)
    #         # Check if the decoded content matches the original content
    #         self.assertEqual(decoded_content.strip(), content.strip())

    def test_count_lines(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Count lines in each temporary file
            line_count = count_lines(content)
            # Check if the counted lines match the number of lines in the content
            self.assertEqual(line_count, content.count("\n") + 1)

    def test_remove_comments(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Remove comments from each temporary file's content
            content_without_comments = remove_comments(content)
            # Check if the resulting content doesn't contain any comments
            self.assertFalse("//" in content_without_comments)
            self.assertFalse("/*" in content_without_comments)

    def test_count_code_lines(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Count lines of code in each temporary file
            code_line_count = count_code_lines(content)
            # Check if the counted lines match the expected number of code lines
            self.assertEqual(code_line_count, content.count("\n") + 1)

    def test_count_comments(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Count lines of comments in each temporary file
            comment_line_count = count_comments(content)
            # Check if the counted lines match the expected number of comment lines
            expected_comment_lines = content.count("//") + content.count("/*")
            self.assertEqual(comment_line_count, expected_comment_lines)

    def test_count_javadoc_comments(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Count lines of Javadoc comments in each temporary file
            javadoc_comment_line_count = count_javadoc_comments(content)
            # Check if the counted lines match the expected number of Javadoc comment lines
            self.assertEqual(javadoc_comment_line_count, content.count("/**"))

    def test_count_functions(self):
        for file_name, content in zip(self.test_files, self.test_contents):
            file_path = os.path.join(self.temp_dir.name, file_name)
            # Count functions in each temporary file's content
            function_count = count_functions(content)
            # Check if the counted functions match the expected number of functions
            expected_function_count = content.count("void")
            self.assertEqual(function_count, expected_function_count)

    def test_calculate_comment_deviation(self):
        # Test calculate_comment_deviation function with mocked metrics
        metrics = {
            FUNCTIONS: 5,
            CODE_LINES: 100,
            JAVADOC_LINES: 3,
            OTHER_COMMENTS: 5,
        }
        deviation = calculate_comment_deviation(metrics)
        self.assertAlmostEqual(deviation, -78.66, delta=0.01)



if __name__ == "__init__":
    unittest.main()
