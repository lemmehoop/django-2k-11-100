from django.http import HttpResponse
from django.shortcuts import render


def main_view(request):
    return render(request, "web/main.html")
