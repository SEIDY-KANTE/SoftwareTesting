import unittest
from unittest.mock import patch
from SoftwareTesting.models.CloneRepository import CloneRepositoryForm
from parameterized import parameterized
import subprocess
from os import environ


"""
This test case class contains unit tests for the CloneRepositoryForm class using mock objects.
"""


class UnittestCloneRepository(unittest.TestCase):

    def test_url_field_validation(self):
        form = CloneRepositoryForm({"url": "not_a_valid_url"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], ["Invalid GitHub URL"])

    @patch("subprocess.run")
    def test_clone_repo_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            [], 0, stdout=b"stdout", stderr=b"stderr"
        )
        form = CloneRepositoryForm(
            {"url": "https://github.com/SEIDY-KANTE/smart-cooling-device"}
        )
        directory = "/path/to/clone/repo"
        success, message = form.clone_repo(directory)

        self.assertTrue(success)
        self.assertEqual(
            message, "Repository cloned successfully to /path/to/clone/repo"
        )
        en = environ.copy()
        en["GIT_TERMINAL_PROMPT"] = "0"

        mock_subprocess_run.assert_called_once_with(
            ["git", "clone", "https://github.com/SEIDY-KANTE/smart-cooling-device"],
            env=en,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_clone_repo_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            [], 1, stdout=b"stdout", stderr=b"stderr"
        )
        form = CloneRepositoryForm(
            {"url": "https://github.com/SEIDY-KANTE/smart-cooling-device"}
        )
        directory = "/path/to/clone/repo"
        success, message = form.clone_repo(directory)

        self.assertFalse(success)
        self.assertEqual(message, "Error cloning repository")
        en = environ.copy()
        en["GIT_TERMINAL_PROMPT"] = "0"

        mock_subprocess_run.assert_called_once_with(
            ["git", "clone", "https://github.com/SEIDY-KANTE/smart-cooling-device"],
            env=en,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_clone_repo_missing_url(self, mock_subprocess_run):
        form = CloneRepositoryForm({"url": ""})
        directory = "/path/to/clone/repo"
        success, message = form.clone_repo(directory)

        self.assertFalse(success)
        self.assertEqual(message, "URL is not provided")
        self.assertFalse(mock_subprocess_run.called)

    @parameterized.expand(
        [
            ("not_a_valid_url", ["Invalid GitHub URL"]),
            ("http://github.com/someuser/somerepo", ["Invalid GitHub URL"]),
            ("https://notgithub.com/someuser/somerepo", ["Invalid GitHub URL"]),
        ]
    )
    def test_url_field_validation(self, url, expected_errors):
        form = CloneRepositoryForm({"url": url})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], expected_errors)

    @parameterized.expand(
        [
            (
                "https://github.com/someuser/somerepo",
                True,
                "Repository cloned successfully to /path/to/clone/repo",
            ),
            (
                "https://github.com/otheruser/anotherrepo",
                False,
                "Error cloning repository",
            ),
        ]
    )
    @patch("subprocess.run")
    def test_clone_repo(self, url, success, expected_message, mock_subprocess_run):
        # Mimic different subprocess.run return values based on test case
        return_code = 0 if success else 1
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            [], return_code, stdout=b"stdout", stderr=b"stderr"
        )
        form = CloneRepositoryForm({"url": url})
        directory = "/path/to/clone/repo"
        success, message = form.clone_repo(directory)

        self.assertEqual(success, success)
        self.assertEqual(message, expected_message)
        en = environ.copy()
        en["GIT_TERMINAL_PROMPT"] = "0"

        mock_subprocess_run.assert_called_once_with(
            ["git", "clone", url],
            env=en,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
