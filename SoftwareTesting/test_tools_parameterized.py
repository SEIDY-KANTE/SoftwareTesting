import unittest
from parameterized import parameterized
from unittest.mock import patch, mock_open
from parameterized import parameterized
from SoftwareTesting.utils.tools import (
    get_java_files,
    count_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    count_code_lines,
    calculate_comment_deviation,
    remove_comments,
    remove_javadoc_comments,
    read_and_decode_file,
)

from SoftwareTesting.utils.config import (
    FUNCTIONS,
    CODE_LINES,
    JAVADOC_LINES,
    OTHER_COMMENTS,
)

class TestToolsParameterized(unittest.TestCase):

    @parameterized.expand(
        [
            (
                "/path/to/directory",
                [
                    "/path/to/directory\\Class1.java",
                    "/path/to/directory\\Class2.java",
                    "/path/to/directory\\Class3.java",
                    "/path/to/directory\\Class4.java",
                ],
            ),
            (
                "/path/to/another/directory",
                [
                    "/path/to/another/directory\\Class1.java",
                    "/path/to/another/directory\\Class2.java",
                    "/path/to/another/directory\\Class3.java",
                    "/path/to/another/directory\\Class4.java",
                ],
            ),
        ]
    )
    @patch("os.walk")
    def test_get_java_files(self, directory_path, expected_result, mock_walk):

        mock_walk.return_value = [
            (
                directory_path,
                [],
                ["Class1.java", "Class2.java", "Class3.java", "Class4.java"],
            )
        ]
        result = get_java_files(directory_path)

        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            ("/path/to/file1.java", "Java file content 1"),
            ("/path/to/file2.java", "Java file content 2"),
            ("/path/to/file3.java", "Java file content 3"),
        ]
    )
    def test_read_and_decode_file(self, file_path, expected_content):
        """Parameterized test to ensure correct reading and decoding of files."""

        # Mock the `open` function to control file contents during testing
        with patch("builtins.open", mock_open(read_data=expected_content)) as mock_file:
            result = read_and_decode_file(file_path)
            mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")

            self.assertEqual(result, expected_content)

    @parameterized.expand(
        [
            (
                "public class Test {// This is a comment    public void method() {/* This is a block comment */}}",
                "public class Test {    public void method() {}}",
            ),
            (
                "public class Test {// Comment 1    public void method() {/* Comment 2 */}}",
                "public class Test {    public void method() {}}",
            ),
            (
                "public class Test {// Comment 1    public void method() {/* Comment 2 */} // Comment 3}",
                "public class Test {    public void method() {}}",
            ),
        ]
    )
    def test_remove_comments(self, sample_content, expected_result):
        # Mock the re.sub function to return a modified content without comments
        with patch("re.sub") as mock_sub:
            mock_sub.return_value = expected_result

            # Call the function with the sample content
            result = remove_comments(sample_content)

            # Assert that the function returned the expected result
            self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            ("Test case 1", "line 1\nline 2\nline 3\n", 3),
            ("Test case 2", "line 1\n", 1),
            ("Test case 3", "", 0),
            ("Test case 4", "line 1\nline 2\nline 3\nline 4\nline 5\n", 5),
        ]
    )
    def test_count_lines(self, name, content, expected_result):
        result = count_lines(content)
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (
                "Test case 1",
                """
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
            """,
                12,
            ),
            (
                "Test case 2",
                """
            public class Test {
                // This is a comment
                public void method() {
                    int x = 5; // This is another comment
                    int y = 10;
                    
                    // Yet another comment
                    if (x < y) {
                        System.out.println("x is less than y");
                    }
                    // Final comment
                }
            }
            """,
                12,
            ),
        ]
    )
    def test_count_code_lines(self, name, sample_content, expected_result):
        result = count_code_lines(sample_content)
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (
                "Test case 1",
                """
                // This is a single-line comment
                // This is another single-line comment
                int x = 5; // This is an inline single-line comment
                int y = 10;
                """,
                3,
            ),
            (
                "Test case 2",
                """
                // This is a single-line comment
                // This is another single-line comment
                // This is a third single-line comment
                int x = 5; // This is an inline single-line comment
                int y = 10;
                """,
                4,
            ),
            (
                "Test case 3",
                """
                int x = 5;
                int y = 10;
                """,
                0,
            ),
        ]
    )
    def test_count_comments(self, mock_findall, sample_content, expected_result):
        # Call the function with the sample content
        result = count_comments(sample_content)

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (
                "Test case 1",
                """
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
        """,
                """
        public class Test {
            // This is a regular comment
            private int x;
            // Another regular comment
            private int y;
        }
        """,
            ),
            (
                "Test case 2",
                """
        /**
            * Sample Javadoc comment.
            */
        public class Test {
            // Regular comment
            private int x;
        }
        """,
                """
        public class Test {
            // Regular comment
            private int x;
        }
        """,
            ),
        ]
    )
    @patch("SoftwareTesting.utils.tools.re.sub")
    def test_remove_javadoc_comments(
        self, _, sample_content, expected_result, mock_sub
    ):
        # Mock the sub method to remove Javadoc comments
        mock_sub.return_value = expected_result

        # Call the function with the sample content
        result = remove_javadoc_comments(sample_content)

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            ("No Javadoc comments", "", 0),
            (
                "Single-line Javadoc comment",
                "/** \n*This is a Javadoc comment.\n */",
                1,
            ),
            (
                "Multi-line Javadoc comment",
                "/**\n* This is a multi-line\n* Javadoc comment.\n */",
                2,
            ),
            (
                "Multiple Javadoc comments",
                """/**
                    * Comment 1
                    * Comment 2 
                    * Comment 3 
                    * Comment 4 
                    * Comment 5 
                    * Comment 6 
                */
                """,
                6,
            ),
        ]
    )
    def test_count_javadoc_comments(self, name, sample_content, expected_result):
        # Mock the match method to control its behavior
        def mock_match(regex, line):
            return bool(line.strip() and line.strip().startswith("*"))

        with patch("SoftwareTesting.utils.tools.re.match", side_effect=mock_match):
            # Call the function with the sample content
            result = count_javadoc_comments(sample_content)

            # Assert that the result matches the expected result
            self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            (
                "sample_code1",
                """
                public class MyClass { private void method1() { // Method 1} }
                """,
                "private void method1()",
            ),
            (
                "sample_code2",
                """
            public class AnotherClass {
            
                public int method2(int param) {
                
                      return 0; 
                }
                protected String method3(String str) { 
                    
                    return ""; 
                }
            }
        """,
                "public int method2(int param)",
            ),
            (
                "sample_code3",
                """
            public class Main {
                // No functions here
            }
        """,
                "",
            ),
        ]
    )
    @patch("re.findall")
    def test_count_functions(self, name, java_content, expected_result, mock_findall):
        """Parameterized test to ensure correct function counting."""

        # Mock the behavior of re.findall to return a list of matched functions
        mock_findall.return_value = expected_result

        # Call the function and assert the result
        result = count_functions(java_content)
        self.assertEqual(result, len(expected_result))

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


if __name__ == "__main__":
    unittest.main()
