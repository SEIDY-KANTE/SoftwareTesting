from SoftwareTesting.CloneRepository import CloneRepositoryForm
from parameterized import parameterized
import unittest
import os

class TestCloneRepositoryForm(unittest.TestCase):

    def remove_repo(self, url):
        repo_dir = url.split("/")[-1]
        repo_path = self.directory + "\\" + repo_dir
        if os.path.exists(repo_path):
            os.chdir(self.directory)
            os.system('rmdir /S /Q "{}"'.format(repo_dir))
            # print(f"\n{repo_dir} is removed\n")

    @classmethod
    def setUpClass(cls):
        cls.directory = os.getcwd()
        cls.url = "https://github.com/SEIDY-KANTE/smart-cooling-device"
        cls.url_failure = cls.url + "/failure"
        cls.form = CloneRepositoryForm(data={"url": cls.url})

    def tearDown(self):
        self.remove_repo(self.url)
        self.remove_repo(self.url_failure)

    def test_valid_url(self):
        self.assertTrue(self.form.is_valid())

    def test_clone_repo(self):

        # Call the clone_repo method
        success, message = self.form.clone_repo(self.directory)

        # Assert
        if success:
            self.assertEqual(
                message, f"Repository cloned successfully to {self.directory}"
            )
        else:
            self.assertEqual(message, "Error cloning repository")

    def test_empty_url(self):
        form = CloneRepositoryForm(data={"url": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], ["This field is required."])

    def test_invalid_github_url(self):
        form = CloneRepositoryForm(data={"url": "https://example.com"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], ["Invalid GitHub URL"])

    def test_invalid_url(self):
        form = CloneRepositoryForm(data={"url": "http://github.com/username/repo"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], ["Invalid GitHub URL"])

    ####################################### PARAMETERIZED #################################

    @parameterized.expand(
        [
            ("https://github.com/SEIDY-KANTE/smart-cooling-device", True),
            ("https://github.com/SEIDY-KANTE/smart-cooling-device/failure", False),
        ]
    )
    def test_clone_repo(self, url, expected_success):
        form = CloneRepositoryForm(data={"url": url})
        success, message = form.clone_repo(self.directory)

        # Assert
        self.assertEqual(success, expected_success)
        if expected_success:
            self.assertEqual(
                message, f"Repository cloned successfully to {self.directory}"
            )
        else:
            self.assertEqual(message, "Error cloning repository")

    @parameterized.expand(
        [
            ("", ["This field is required."]),
            ("https://example.com", ["Invalid GitHub URL"]),
            ("http://github.com/username/repo", ["Invalid GitHub URL"]),
        ]
    )
    def test_invalid_url(self, url, expected_errors):
        form = CloneRepositoryForm(data={"url": url})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["url"], expected_errors)

    @parameterized.expand(
        [
            (
                "Valid_URL",
                {"url": "https://github.com/SEIDY-KANTE/smart-cooling-device"},
                True,
            ),
            ("Empty_URL", {"url": ""}, False),
            ("Invalid_GitHub_URL", {"url": "https://example.com"}, False),
            ("Invalid_URL", {"url": "http://github.com/username/repo"}, False),
        ]
    )
    def test_url_validation(self, name, data, expected_validity):
        form = CloneRepositoryForm(data=data)
        self.assertEqual(form.is_valid(), expected_validity)



if __name__ == "__init__":
    unittest.main()