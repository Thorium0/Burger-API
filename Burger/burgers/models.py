from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from PIL import Image
from multiselectfield import MultiSelectField
import requests






class CustomBurger(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = MoneyField(max_digits=15, decimal_places=2, default_currency='DKK')
    #info = models.TextField(max_length=500)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='burger_pics/', default='default-burger.png')
    creationDate = models.DateTimeField(auto_now=True)

    meatjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/meat-all").json()
    MEATS = ()
    for meat in meatjson:
        MEATS += (meat.get('id'), meat.get('name')),

    bunjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/bun-all").json()
    BUNS = ()
    for bun in bunjson:
        BUNS += (bun.get('id'), bun.get('name')),

    condimentjson = requests.get(url="http://localhost:9000/api/v1/menu/burger/condiment-all").json()
    CONDIMENTS = ()
    for condiment in condimentjson:
        CONDIMENTS += (condiment.get('id'), condiment.get('name')),


    meats = MultiSelectField(choices=MEATS)
    buns = MultiSelectField(choices=BUNS)
    condiments = MultiSelectField(choices=CONDIMENTS)




    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save()
        if not self.image.path: self.image.path = "default-burger.png"
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            size = (500, 500)
            img.thumbnail(size)
            img.save(self.image.path)
