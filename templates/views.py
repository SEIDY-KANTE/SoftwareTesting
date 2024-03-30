from django.shortcuts import render
from django.http import HttpResponse
from SoftwareTesting.models import Metrics
from SoftwareTesting.CloneRepository import CloneRepositoryForm


def index(request):

    if request.method == "POST":

        metrics = Metrics.objects.all()
        metric = CloneRepositoryForm(request.POST)

        if metric.is_valid():
            (is_cloned, message) = metric.clone_repo()
            # print("INPUT URL: ", request.POST["url"])

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
