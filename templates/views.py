from django.shortcuts import render
from django.http import HttpResponse
from SoftwareTesting.models import Metrics


def index(request):
    metrics = Metrics.objects.all()
    return render(request, "index.html", {"metrics": metrics})
