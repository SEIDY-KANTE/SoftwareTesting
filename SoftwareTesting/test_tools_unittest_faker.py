import unittest
from unittest.mock import patch
from faker import Faker
from SoftwareTesting.utils.tools import (
    get_java_files,
    count_lines,
    count_code_lines,
    count_comments,
    count_javadoc_comments,
    count_functions,
    remove_comments,
    remove_javadoc_comments,
)


class ToolsUnittestWithFaker(unittest.TestCase):
    @patch("os.walk")
    def test_get_java_files(self, mock_walk):
        # Initialize Faker
        fake = Faker()

        # Generate fake file names
        fake_file_names = [fake.file_name() + ".java" for _ in range(4)]

        # Set up the fake directory structure
        fake_directory = "/path/to/fake_directory"
        fake_files = [(fake_directory, [], fake_file_names)]

        # Mock os.walk to return the fake directory structure
        mock_walk.return_value = fake_files

        # Call the function under test
        result = get_java_files(fake_directory)

        # Define the expected result
        expected_result = [
            fake_directory + "\\" + file_name
            for file_name in fake_file_names
            if not file_name.startswith("I")
        ]

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_count_lines(self):
        # Generate fake content with faker
        fake = Faker()
        fake_content = "\n".join([fake.sentence() for _ in range(100)])

        # Call the function under test
        result = count_lines(fake_content)

        # Define the expected result
        expected_result = 100

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_count_code_lines(self):
        # Create a Faker instance
        faker = Faker()

        content = f"""
                public class {faker.word().capitalize()} {{
                            // {faker.word()}
                            public void {faker.word().capitalize()}() {{
                                int x = 5; // {faker.word()}
                                int y = 10;

                                // {faker.word()}
                                if (x > y) {{
                                    System.out.println({{}});
                                }}
                                // {faker.word()}
                            }}
                        }}
                """

        content = remove_comments(content)
        result = count_code_lines(content)

        # Define the expected result (number of lines containing actual code)
        expected_result = 9

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.findall")
    def test_count_comments(self, mock_findall):
        # Create a Faker instance
        faker = Faker()

        word = faker.word()
        sentence = faker.sentence()

        # Generate a fake Java content string
        sample_content = f"""
        // {word}
        // {sentence}
        int x = 5; // {word}
        int y = 10;
        """

        # Mock the findall method to return a predefined result
        mock_findall.return_value = [
            "//" + word,
            "//" + sentence,
            "//" + word,
        ]

        # Call the function with the sample content
        result = count_comments(sample_content)

        # Define the expected result (number of single-line comments)
        expected_result = 3 

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.sub")
    def test_remove_javadoc_comments(self, mock_sub):
        # Create a Faker instance
        faker = Faker()
        word = faker.word()

        # Generate Javadoc comments and Java content string
        javadoc_comments = [faker.sentence() for _ in range(3)]
        sample_content = (
            "\n".join(["/** " + comment + " */" for comment in javadoc_comments])
            + f""" 
            public class {word.capitalize()} {{
            //  {word}
            private int x;
            //  {word}
            private int y;
        }}
        """
        )

        # Mock the sub method to remove Javadoc comments
        mock_sub.return_value = f"""
         public class {word.capitalize()} {{
            //  {word}
            private int x;
            //  {word}
            private int y;
        }}
        """

        # Call the function with the sample content
        result = remove_javadoc_comments(sample_content)

        # Define the expected result (content without Javadoc comments)
        expected_result = f"""
         public class {word.capitalize()} {{
            //  {word}
            private int x;
            //  {word}
            private int y;
        }}
        """

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    @patch("SoftwareTesting.utils.tools.re.match")
    def test_count_javadoc_comments(self, mock_match):
        # Create a Faker instance
        faker = Faker()

        # Generate Javadoc comments
        javadoc_comments = [faker.sentence() for _ in range(3)]
        javadoc_comments_str = "\n/**" + "\n*".join(javadoc_comments) + "\n*/"

        # Define a sample Javadoc content string
        sample_content = f"{javadoc_comments_str}\n\npublic class {faker.word().capitalize()} {{{javadoc_comments_str}\n}}\n"

        # Mock the match method to only match lines starting with "*"
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
        # Create a Faker instance
        faker = Faker()

        # Generate fake function declarations
        functions = [
            f"{faker.word()} {faker.word()} {faker.word()}() {{ {faker.sentence()} }}",
            f"{faker.word()} {faker.word()}({faker.word()} {faker.word()}) {{ {faker.sentence()} }}",
            f"{faker.word()} {faker.word()} {faker.word()}({faker.word()} {faker.word()}) {{ {faker.sentence()} }}",
        ]

        # Concatenate the function declarations into a sample Java content string
        sample_content = "\n\n".join(functions)

        # Mock the behavior of re.findall to return a list of matched functions
        mock_findall.return_value = functions

        # Call the function with the sample content
        result = count_functions(sample_content)

        # Assert that the function returned the expected result
        expected_result = 3  # Expected number of declared functions
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
