import os

from urllib.request import urlopen, Request
from urllib.error import URLError


BASE_URL = "127.0.0.1"

DIRECTORY = os.getcwd()

FILENAME = "ClassName"
JAVADOC_LINES = "JavaDocLines"
OTHER_COMMENTS = "OtherComments"
CODE_LINES = "CodeLines"
LOC = "Loc"  # Lines of Code (LOC)
FUNCTIONS = "FunctionLines"
COMMENT_DEVIATION = "CommentDeviation"


def internet_on():
    try:
        # urlopen(BASE_URL + ":8000", timeout=1)
        url = "https://api.github.com/"
        request = Request(url)
        response = urlopen(request)
        # data_content = response.read()
        # print(data_content)
        return True
    except URLError as err:
        return False


INTERNET_CONNECTION = ""

if internet_on():
    INTERNET_CONNECTION = "ON"
    # print("Connection successful")
else:
    INTERNET_CONNECTION = "OFF"
    # print("No connection")
