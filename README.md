# SoftwareTesting

**Project Name:** JAVA CODE ANALYZER

**Project Description:**
GitHub Java Code Analyzer is a Django web application that analyzes Java classes from a GitHub repository specified by the user and reports specific metrics. After the user enters the URL of a GitHub repository, the application clones the repository, extracts Java classes, and calculates the following metrics for each class:

- Number of Javadoc lines
- Number of other comment lines
- Number of code lines (excluding comments and empty lines)
- LOC (Line of Code) (Total lines)
- Number of functions
- Comment deviation percentage

These metrics are calculated separately for each class and presented to the user. Additionally, previously conducted analyses are retrieved from the database and presented to the user.

**Technologies Used:**

- Django Framework
- PostgreSQL
- HTML/CSS/JavaScript
- Faker Library (for unit tests)
- tempfile Library
- Unittest and Parametrized Test (for unit and integration tests)

**Features:**

- Accepts GitHub repository URL from the user.
- Clones the repository and retrieves \*.java files.
- Parses classes and calculates specific metrics.
- Stores analysis results in the database and presents them to the user.
- Displays the history of previous analyses to the user.

**Tests:**

A total of approximately 85 tests have been conducted:
- 41 unit tests have been written.
  - 7 of them utilize the Faker library.
  - 10 of them use parameterized tests.
- 19 integration tests have been written.
  - 3 of them utilize parameterized tests.

**Screenshots from the Project:**

<div >
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/home_page.png" alt="Home Page" width="400"  />
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/result_page.png" alt="Result Page" width="400"  />
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/error_cloning_page.png" alt="Error Cloning Page" width="400"  />
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/invalid_form_page.png" alt="Invalid Form Page" width="400"  />
   <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/test_output.png" alt="Test Output" />
</div>

***When there is a problem with the internet connection, it may cause an issue during the cloning test. Therefore, I found a solution that checks the internet connection, and if there is a problem, it skips the cloning test.***
<div >
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/internet_connection_checker.png" alt="Internet Connection Checker" width="400"  />
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/clone_repo.png" alt="Clone Repo Test" width="400"  />
  <img src="https://github.com/SEIDY-KANTE/SoftwareTesting/blob/main/Screenshots/connection_off_output.png" alt="Connection OFF Output" />
</div>

**Conclusion:**
GitHub Java Class Analyzer automates the analysis of Java classes, saving time for developers and improving code quality. Both unit tests and integration tests provide a comprehensive testing process to ensure the accuracy and reliability of the application.

## How to Use

1. Clone the project repository:

```bash
git clone https://github.com/SEIDY-KANTE/SoftwareTesting.git
```

2. Navigate to the project directory:

```bash
cd SoftwareTesting
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

For Unix/Linux:

```bash
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Create the PostgreSQL database and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run the Django server:

```bash
python manage.py runserver
```

7. Open your browser and go to `http://127.0.0.1:8000/` to analyze GitHub repositories using the user interface.
