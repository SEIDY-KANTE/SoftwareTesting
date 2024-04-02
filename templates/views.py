from django.shortcuts import render
from django.http import HttpResponse
from SoftwareTesting.models import Metrics
from SoftwareTesting.CloneRepository import CloneRepositoryForm
from SoftwareTesting.tools import get_java_files
from SoftwareTesting.Analyzer import Analyzer
from django.db import transaction
from SoftwareTesting.config import DIRECTORY


def index(request):

    if request.method == "POST":

        metric = CloneRepositoryForm(request.POST)

        # print(len(metrics))

        if metric.is_valid():
            (is_cloned, message) = metric.clone_repo(DIRECTORY)
            # print("INPUT URL: ", request.POST["url"])

            java_files = get_java_files(DIRECTORY)
            # index = 0
            with transaction.atomic():
                for file in java_files:
                    analyzed_data = Analyzer.analyze(file)
                    # index += 1
                    metrics = Metrics(**analyzed_data)
                    metrics.save()

                    # print(f"\n==================={index}. {file} ===================\n")
                    # print(analyzed_data)

            metrics = Metrics.objects.all()

            if is_cloned:
                return render(request, "Result.html", {"metrics": metrics})

            else:
                return HttpResponse(
                    f"""<h1>⚠️Error Cloning Repository</h1>
                        <h3>{message}</h3>
                        <h4> Is repo already cloned ? <a href = 'result/'>See Result ⏩<a>  </h4>
                        <a href='/'>Go Back 🔙</a>"""
                )

        else:
            return HttpResponse(
                """<h1>⛔Invalid Form</h1>
                    <br>
                    <h3>⚠️Please enter a valid GitHub URL</h3>
                <a href='/'>Go Back 🔙</a>"""
            )

    return render(request, "index.html")


def result(request):
    metrics = Metrics.objects.all()
    return render(request, "Result.html", {"metrics": metrics})
