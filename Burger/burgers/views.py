from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .forms import CustomBurgerCreationForm
from .models import CustomBurger
import requests


@login_required
def burgerList(request):
    burgersObj = CustomBurger.objects.all()
    burgers = []
    if request.user.is_superuser:
        burgers = burgersObj
    else:
        for burger in burgersObj:
            if burger.creator == request.user:
                burgers.append(burger)


    context = {
    "title" : "Burgers",
    "burgers" : burgers,
    "editBtn": True
    }
    return render(request, 'burgers/burgers.html.django', context)


@login_required
def delBurger(request, id):
    try: burger = CustomBurger.objects.get(id=id)
    except: pass
    else:
        if burger.creator == request.user or request.user.is_superuser:
            burger.delete()
    return redirect("burgers")


@login_required
def editBurger(request, id):
    burger = CustomBurger.objects.get(id=id)
    if burger.creator == request.user or request.user.is_superuser:
        if request.method == 'POST':
            form = CustomBurgerCreationForm(request.POST, request.FILES, instance=burger)
            if form.is_valid():
                form.save()
                messages.success(request, 'Burger updated!')
                return redirect('burgers')

        else:
            form = CustomBurgerCreationForm(instance=burger)

        context = {
        "title": "Edit Burger",
        "topTitle" : "Edit Burger",
        "btnName" : "Update",
        "form": form,
        "burger": burger
        }
        return render(request, 'burgers/addBurger.html.django', context)
    else:
        return redirect('burgers')


@login_required
def addBurger(request):
    if request.method == 'POST':
        form = CustomBurgerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            burger = form.save(commit=False)
            burger.creator = request.user

            
            try: burger.save()
            except: messages.error(request, "Error")
            else: messages.success(request, "Burger created!")
            return redirect('burgers')

    else:
        form = CustomBurgerCreationForm()
    context = {
    "title" : "Create Burger",
    "topTitle" : "Create Burger",
    "btnName" : "Submit",
    "form" : form
    }
    return render(request, 'burgers/addBurger.html.django', context)




@login_required
def displayBurger(request, id):
    burger = CustomBurger.objects.get(id=id)

    jsonLinks = [
    "http://localhost:9000/api/v1/menu/burger/meat-all",
    "http://localhost:9000/api/v1/menu/burger/bun-all",
    "http://localhost:9000/api/v1/menu/burger/condiment-all",
    "http://localhost:9000/api/v1/menu/burger/salad-all"
    ]

    try:
        PARTS = []
        for link in range(len(jsonLinks)):
            partjson = requests.get(url=jsonLinks[link]).json()
            PARTS.append({})
            for part in partjson:
                PARTS[link][part.get('id')] = part.get('name')
    except:
        messages.warning(request, "API is offline")
        return redirect('burgers')


    meats = []
    for id in burger.meats:
        meats.append(PARTS[0][int(id)])

    buns = []
    for id in burger.buns:
        buns.append(PARTS[1][int(id)])

    condiments = []
    for id in burger.condiments:
        condiments.append(PARTS[2][int(id)])

    salads = []
    for id in burger.salads:
        salads.append(PARTS[3][int(id)])

    context = {
    "title": burger.title,
    "burger": burger,
    "meats": meats,
    "buns": buns,
    "condiments": condiments,
    "meats": meats,
    "salads": salads,
    "currentUser" : request.user,
    }
    return render(request, 'burgers/displayBurger.html.django', context)
