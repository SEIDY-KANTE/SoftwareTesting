import unittest
from unittest.mock import patch, mock_open
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


class UnittestTools(unittest.TestCase):

    @patch("os.walk")
    def test_get_java_files(self, mock_walk):
        mock_walk.return_value = [
            (
                "/path/to/directory",
                [],
                ["Class1.java", "IInterface1.java", "Class2.java", "IInterface2.java"],
            )
        ]
        result = get_java_files("/path/to/directory")
        expected_result = [
            "/path/to/directory\\Class1.java",
            "/path/to/directory\\Class2.java",
        ]
        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=mock_open, read_data="Java file content")
    def test_read_and_decode_file(self, mock_open):
        result = read_and_decode_file("/path/to/java_file.java")
        expected_result = "Java file content"
        self.assertEqual(result, expected_result)

    def test_count_lines(self):
        content = "line 1 \nline 2 \nline 3"
        result = count_lines(content)
        expected_result = 3
        self.assertEqual(result, expected_result)

    @patch("re.sub")
    def test_remove_comments(self, mock_sub):
        # Mock the re.sub function to return a modified content without comments
        mock_sub.return_value = "public class Test {    public void method() {}}"

        # Call the function with a sample content
        result = remove_comments(
            "public class Test {// This is a comment    public void method() {/* This is a block comment */}}"
        )

        # Assert that the function returned the expected result
        expected_result = "public class Test {    public void method() {}}"
        self.assertEqual(result, expected_result)

    def test_count_code_lines(self):
        # Define a sample Java content string with comments and whitespace
        sample_content = """
        public class Test {
            // This is a comment
            public void method() {
                int x = 5; // This is another comment
                int y = 10;
                
                // Yet another comment
                if (x > y) {
                    System.out.println("x is greater than y");
                }
                // Final comment
            }
        }
        """

        sample_content = remove_comments(sample_content)
        # Call the function with the sample content
        result = count_code_lines(sample_content)

        # Define the expected result (number of lines containing actual code)
        expected_result = 9 

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.findall")
    def test_count_comments(self, mock_findall):
        # Define a sample Java content string
        sample_content = """
        // This is a single-line comment
        // This is another single-line comment
        int x = 5; // This is an inline single-line comment
        int y = 10;
        """

        # Mock the findall method to return a predefined result
        mock_findall.return_value = [
            "// This is a single-line comment",
            "// This is another single-line comment",
            "// This is an inline single-line comment",
        ]

        # Call the function with the sample content
        result = count_comments(sample_content)

        # Define the expected result (number of single-line comments)
        expected_result = 3 

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.sub")
    def test_remove_javadoc_comments(self, mock_sub):
        # Define a sample Java content string with Javadoc comments
        sample_content = """
        /**
         * This is a Javadoc comment.
         * It spans multiple lines.
         */
        public class Test {
            // This is a regular comment
            private int x;
            // Another regular comment
            private int y;
        }
        """

        # Mock the sub method to remove Javadoc comments
        mock_sub.return_value = """
        public class Test {
            // This is a regular comment
            private int x;
            // Another regular comment
            private int y;
        }
        """

        # Call the function with the sample content
        result = remove_javadoc_comments(sample_content)

        # Define the expected result (content without Javadoc comments)
        expected_result = """
        public class Test {
            // This is a regular comment
            private int x;
            // Another regular comment
            private int y;
        }
        """

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.match")
    def test_count_javadoc_comments(self, mock_match):
        # Define a sample Javadoc content string
        sample_content = """
        /**
         * This is a sample Javadoc comment.
         * It spans multiple lines.
         */

        /**
         * Another Javadoc comment.
         * With multiple lines.
         * And more lines.
         */

        /**
            * Third Javadoc comment.
        */

        """

        # Mock the match method to control its behavior
        # Mock the behavior of re.match to only match lines starting with "*"
        def mock_match(regex, line):
            return bool(line.strip() and line.strip().startswith("*"))

        mock_match.side_effect = mock_match

        # Call the function with the sample content
        result = count_javadoc_comments(sample_content)

        # Define the expected result (number of lines in Javadoc comments)
        expected_result = 6

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("re.findall")
    def test_count_functions(self, mock_findall):
        # Define a sample Java content string with function declarations
        sample_content = """
        public class MyClass {

            private void method1() {
                // Method 1
            }

            public int method2(int param) {
                // Method 2
                return param * 2;
            }

            protected String method3(String str) {
                // Method 3
                return "Hello, " + str;
            }
        }
        """

        # Mock the behavior of re.findall to return a list of matched functions
        mock_findall.return_value = [
            "private void method1()",
            "private int method2()",
            "protected String method3()",
        ]

        # Call the function with a sample content
        result = count_functions(sample_content)

        # Assert that the function returned the expected result
        expected_result = 3  # Expected number of declared functions
        self.assertEqual(result, expected_result)

    def test_comment_deviation_with_valid_metrics(self):
        # Define a sample metrics dictionary with valid values
        metrics = {
            FUNCTIONS: 10,
            CODE_LINES: 100,
            JAVADOC_LINES: 20,
            OTHER_COMMENTS: 30,
        }

        # Call the function with the sample metrics
        result = calculate_comment_deviation(metrics)

        # Define the expected result
        expected_result = 33.3333333333  # Calculated manually

        # Assert that the result matches the expected result with a tolerance of 1e-6
        self.assertAlmostEqual(result, expected_result, delta=1e-6)

    def test_comment_deviation_with_zero_functions(self):
        # Define a sample metrics dictionary with zero functions
        metrics = {
            FUNCTIONS: 0,
            CODE_LINES: 100,
            JAVADOC_LINES: 20,
            OTHER_COMMENTS: 30,
        }

        # Call the function with the sample metrics
        result = calculate_comment_deviation(metrics)

        # Define the expected result (zero deviation)
        expected_result = 0.0

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_comment_deviation_with_zero_code_lines(self):
        # Define a sample metrics dictionary with zero code lines
        metrics = {
            FUNCTIONS: 10,
            CODE_LINES: 0,
            JAVADOC_LINES: 20,
            OTHER_COMMENTS: 30,
        }

        # Call the function with the sample metrics
        result = calculate_comment_deviation(metrics)

        # Define the expected result (zero deviation)
        expected_result = 0.0

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
