from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from SoftwareTesting.models import Metrics
from SoftwareTesting.CloneRepository import CloneRepositoryForm
from SoftwareTesting.tools import get_java_files
from SoftwareTesting.Analyzer import Analyzer
from SoftwareTesting.config import DIRECTORY

def index(request):
    if request.method == "POST":
        # Process form submission
        clone_form = CloneRepositoryForm(request.POST)
        if clone_form.is_valid():

            # Clone repository and analyze Java files
            is_cloned, message = clone_form.clone_repo(DIRECTORY)
            # If cloning was successful, analyze Java files and save metrics
            java_files = get_java_files(DIRECTORY)
            with transaction.atomic():
                for file in java_files:
                    analyzed_data = Analyzer.analyze(file)
                    metrics = Metrics(**analyzed_data)
                    metrics.save()

            # Fetch all metrics from the database
            metrics = Metrics.objects.all()
            
            if is_cloned:
                # Render the result template with metrics
                return render(request, "Result.html", {"metrics": metrics})
            else:
                # If cloning failed, display error message
                error_message = (
                    f"<div style='text-align: center; color: red;'>"
                    f"<h1>⚠️{message}</h1>"
                    f"<h3  style='color: green;'>Is repo already cloned? <a href='/result/'>See Result ⏩</a></h3>"
                    f"<a href='/'>Go Back 🔙</a>"
                    f"</div>"
                )
                return HttpResponse(error_message)
        else:
            # If form submission is invalid, display error message
            error_message = (
                "<div style='text-align: center; color: red;'>"
                "<h1>⛔Invalid Form</h1>"
                "<br>"
                "<h3>⚠️Please enter a valid GitHub URL</h3>"
                "<a href='/'>Go Back 🔙</a>"
                "</div>"
            )
            return HttpResponse(error_message)
    # Render the index template for GET requests
    return render(request, "index.html")

def result(request):
    # Fetch all metrics from the database and render the result template
    metrics = Metrics.objects.all()
    return render(request, "Result.html", {"metrics": metrics})
