from SoftwareTesting.utils.config import *
import os
import re


def get_java_files(directory):
    """
    Retrieves all files with the .java extension within a DIRECTORY.
    Excludes files representing Java interfaces that start with "I".

    Returns:
        list: A list of absolute paths to all discovered Java files excluding interfaces.
    """
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                # Check if the file represents an interface
                if not file.startswith("I"):
                    java_files.append(os.path.join(root, file))
                # Check if the file represents a class and not an interface
                elif file.startswith("I") and file[1].islower():
                    java_files.append(os.path.join(root, file))

    return java_files


def read_and_decode_file(file_path):
    """Reads a file and decodes its content (assuming UTF-8 encoding).

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The decoded content of the file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def count_lines(content):
    """
    Counts the total lines of code in a Java class file.

    Args:
        content (str): The decoded content of the Java class file.

    Returns:
        int: The total number of lines in the file.
    """

    return len(content.splitlines())


def remove_comments(content):
    """
    Removes all comments from Java content.

    Args:
        content (str): The Java content string.

    Returns:
        str: The Java content string with comments removed.
    """

    # Regular expressions for comments
    comment_pattern = r"(//.*?$|/\*.*?\*/)"

    # Remove comments
    code_without_comments = re.sub(
        comment_pattern, "", content, flags=re.MULTILINE | re.DOTALL
    )

    return code_without_comments


def count_code_lines(content):
    """
    Counts the lines of actual code in a Java class file (excluding comments and whitespace).

    Args:
        content (str): The decoded content of the Java class file.

    Returns:
        int: The number of lines containing actual code.
    """

    code_lines = []
    for line in content.splitlines():
        if line.strip():
            code_lines.append(line)

    return len(code_lines)


def count_comments(content):
    """
    Counts the total lines of comments (excluding Javadoc comments) in a Java class file.

    Args:
        content (str): The decoded content of the Java class file.

    Returns:
        int: The number of lines containing comments (other than Javadoc).
    """

    # Regular expression pattern for single-line comments
    single_line_comment_pattern = r"(?s)//.*?"

    # Count single-line comments
    single_line_comments_count = len(re.findall(single_line_comment_pattern, content))

    return single_line_comments_count


def remove_javadoc_comments(content):
    """
    Removes Javadoc comments from Java content.

    Args:
        content (str): The Java content string.

    Returns:
        str: The Java content string with Javadoc comments removed.
    """

    # Regular expression pattern for Javadoc comments
    javadoc_comment_pattern = r"/\*\*.*?\*/"

    # Remove Javadoc comments
    code_without_javadoc_comments = re.sub(
        javadoc_comment_pattern, "", content, flags=re.MULTILINE | re.DOTALL
    )

    return code_without_javadoc_comments


def count_javadoc_comments(content):
    """
    Counts the number of lines in a Javadoc content.

    Args:
        content (str): The Javadoc content as a string.

    Returns:
        int: The number of lines in the Javadoc content.
    """
    # Regular expression pattern for Javadoc content lines
    javadoc_line_regex = r"^\s*\*.*$"

    # Split the lines of the Javadoc content
    lines = content.strip().split("\n")

    # Filter lines of the Javadoc content
    javadoc_lines = [
        line
        for line in lines
        if line.strip()
        and not line.strip().startswith("/*")
        and not line.strip().endswith("*/")
    ]

    # Count lines matching the Javadoc line regex
    javadoc_lines_count = sum(
        1 for line in javadoc_lines if re.match(javadoc_line_regex, line)
    )

    return javadoc_lines_count


def count_functions(content):
    """
    Counts the number of functions declared in a Java class file.

    Args:
        content (str): The decoded content of the Java class file.

    Returns:
        int: The number of declared functions.
    """

    function_pattern = r"((public|private|protected|static|final|native|synchronized|abstract|transient)+\s?)+[\$_\w\<\>\w\s\[\]]*\s+[\$_\w]+\([^\)]*\)?\s*"

    return len(re.findall(function_pattern, content, re.DOTALL))


def calculate_comment_deviation(metrics):
    """
    Calculates the comment deviation metric based on other metrics.

    Args:
        metrics (dict): A dictionary containing code metrics for the analyzed class.

    Returns:
        float: The calculated comment deviation value.
    """

    if metrics[FUNCTIONS] != 0 and metrics[CODE_LINES] != 0:
        yg = (
            (metrics[JAVADOC_LINES] + metrics[OTHER_COMMENTS])
            * 0.8
            / metrics[FUNCTIONS]
        )
        yh = metrics[CODE_LINES] / metrics[FUNCTIONS] * 0.3
        return (100 * yg) / yh - 100
    else:
        return 0.0
