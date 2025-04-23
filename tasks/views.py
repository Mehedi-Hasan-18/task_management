from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
    #Work with database
    # Transform data
    # Data pass
    # Http response / Json response
def home(request):
    return HttpResponse("Welcome to the task management")
    
def contact(recquest):
    return HttpResponse("This is Contact page")

def show_details(request):
    return HttpResponse("This is Show Details section")