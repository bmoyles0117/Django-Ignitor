from django.shortcuts import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World from Django View")