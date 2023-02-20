from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    context ={
        'title': home,
        'discription':'it is a home page'
    }
    return render(request,'home/home.html',context)

def contact(request):
    context ={
        'title': contact,
        'discription':'it is a contact page'
    }
  
    return render(request,'home/contact.html',context)
