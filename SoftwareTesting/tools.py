from SoftwareTesting.config import *
import os
import re


def get_java_files(directory):
    """
    Retrieves all files with the .java extension within a DIRECTORY.

    Returns:
        list: A list of absolute paths to all discovered Java files.
    """

    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def read_and_decode_file(filename):
    """
    Reads the content of a Java class file and decodes it to a string.

    Args:
        filename (str): Path to the Java class file.

    Returns:
        str: The decoded content of the Java class file.
    """

    with open(filename, "rb") as file:
        content = file.read()
        return content.decode("utf-8")


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

    other_comment = r"(?s)//.*?$|/\*.*?\*/"
    return len(re.findall(other_comment, content, re.MULTILINE | re.DOTALL))


def count_javadoc_comments(content):
    """
    Counts the lines of Javadoc comments in a Java class file.

    Args:
        content (str): The decoded content of the Java class file.

    Returns:
        int: The number of lines containing Javadoc comments.
    """

    javadoc_comment = r"/\*\*.*?\*/"
    return len(re.findall(javadoc_comment, content, re.DOTALL | re.MULTILINE))


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
