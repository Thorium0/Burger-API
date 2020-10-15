from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from validate_email import validate_email



def home(request):
    context = {
    "title" : "Home"
    }
    return render(request, 'main/home.html.django', context)


def faq(request):
    txtFile = default_storage.open('faq.html', 'r')
    faq = txtFile.read()
    txtFile.close()
    context = {
    "title" : "FAQ",
    "faq": faq
    }
    return render(request, 'main/faq.html.django', context)


def about(request):
    context = {
    "title" : "About us",
    }
    return render(request, 'main/about.html.django', context)


def spa(request):
    context = {
    "title" : "SPA",
    }
    return render(request, 'main/spa.html.django', context)
