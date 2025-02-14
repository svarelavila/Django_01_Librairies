from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect


def hello_world(request):
    return HttpResponse("Hello World!")

def home_redirect(request):
    return redirect('/helloworld/')