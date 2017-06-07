from django.shortcuts import render

def index(request):
    return HttpResponse("<a href='api/v1'>API</a>")
