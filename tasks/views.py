from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return HttpResponse("Hello, User! Your To‑Do List app is ready 📝")
# Create your views here.
