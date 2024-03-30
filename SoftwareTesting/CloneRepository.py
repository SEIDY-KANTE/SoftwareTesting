from django import forms
from django.core.validators import URLValidator
import os
import subprocess
from os import environ


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

    def clone_repo(self):

        url = self.cleaned_data["url"]

        directory = os.getcwd()
        en = environ.copy()
        en["GIT_TERMINAL_PROMPT"] = "0"
        try:
            completed = subprocess.run(["git", "clone", url], env=en)

            if completed.returncode != 0:
                return (False, f"Uppps!! Error {completed.returncode}!")

            return (True, f"Repository cloned successfully to {directory}")

        except subprocess.CalledProcessError as error:
            return (False, f"Error cloning repository: {error}")
