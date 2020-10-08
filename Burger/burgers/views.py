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
                messages.success(request, 'Sale Updated!')
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
            burger.isSold = False

            try: burger.save()
            except: messages.error(request, "Error")
            else: messages.success(request, "Sale Created!")
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

    try:
        meatjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/meat-all").json()
        MEATS = {}
        for meat in meatjson:
            MEATS[meat.get('id')] = meat.get('name')

        bunjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/bun-all").json()
        BUNS = {}
        for bun in bunjson:
            BUNS[bun.get('id')] = bun.get('name')

        condimentjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/condiment-all").json()
        CONDIMENTS = {}
        for condiment in condimentjson:
            CONDIMENTS[condiment.get('id')] = condiment.get('name')
    except:
        messages.warning(request, "API is offline")
        return redirect('burgers')


    meats = []
    for id in burger.meats:
        meats.append(MEATS[int(id)])

    buns = []
    for id in burger.buns:
        buns.append(BUNS[int(id)])

    condiments = []
    for id in burger.condiments:
        condiments.append(CONDIMENTS[int(id)])

    context = {
    "title": burger.title,
    "burger": burger,
    "meats": meats,
    "buns": buns,
    "condiments": condiments,
    "meats": meats,
    "currentUser" : request.user,
    }
    return render(request, 'burgers/displayBurger.html.django', context)
