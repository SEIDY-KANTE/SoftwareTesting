from SoftwareTesting.tools import (
    read_and_decode_file,
    count_lines,
    count_javadoc_comments,
    count_comments,
    remove_comments,
    count_code_lines,
    count_functions,
    calculate_comment_deviation,
)
from SoftwareTesting.config import *


class Analyzer:

    @staticmethod
    def analyze(filename):

        # Initialize metrics
        metrics = {
            FILENAME: filename.split("\\")[-1],
            JAVADOC_LINES: 0,
            OTHER_COMMENTS: 0,
            CODE_LINES: 0,
            LOC: 0,  # Lines of Code (LOC)
            FUNCTIONS: 0,
            COMMENT_DEVIATION: 0.0,
        }

        content = read_and_decode_file(filename)

        metrics[LOC] = count_lines(content)
        metrics[JAVADOC_LINES] = count_javadoc_comments(content)
        metrics[OTHER_COMMENTS] = count_comments(content) - metrics[JAVADOC_LINES]
        filtred_content = remove_comments(content)
        metrics[CODE_LINES] = count_code_lines(filtred_content)

        metrics[FUNCTIONS] = count_functions(content)

        metrics[COMMENT_DEVIATION] = calculate_comment_deviation(metrics)

        return metrics
