from django import forms
from django.core.validators import URLValidator
import os
import subprocess
from os import environ
from SoftwareTesting.utils.config import DIRECTORY


class CloneRepositoryForm(forms.Form):

    url = forms.CharField(
        label="GitHub Repository URL",
        max_length=100,
        validators=[
            URLValidator(
                schemes=["https"],
                regex=r"^https://github.com/.+/.+$",
                message="Invalid GitHub URL",
            )
        ],
    )

    def clone_repo(self, directory):

        url = self.data.get("url")  # Using .get() to avoid KeyError

        if not url:
            return (False, "URL is not provided")

        en = environ.copy()
        en["GIT_TERMINAL_PROMPT"] = "0"
        try:
            completed = subprocess.run(
                ["git", "clone", url], env=en, capture_output=True, text=True
            )

            if completed.returncode != 0:

                # return (
                #     False,
                #     completed.stderr.strip(),
                # )

                return (False, "Error cloning repository")

            return (True, f"Repository cloned successfully to {directory}")

        # except subprocess.CalledProcessError as error:
        #     return (False, f"Error cloning repository")
        except:
            return (False, "Error cloning repository")
