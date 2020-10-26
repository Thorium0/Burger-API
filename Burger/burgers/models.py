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

    jsonLinks = [
    "http://localhost:9000/api/v1/menu/burger/meats-all",
    "http://localhost:9000/api/v1/menu/burger/buns-all",
    "http://localhost:9000/api/v1/menu/burger/condiments-all",
    "http://localhost:9000/api/v1/menu/burger/salads-all",
    "http://localhost:9000/api/v1/menu/burger/cheeses-all"
    ]

    for link in range(len(jsonLinks)):
        partjson = requests.get(url=jsonLinks[link]).json()
        PARTS = ()
        for part in partjson:
            PARTS += (part.get('id'), part.get('name')),
        if link == 0:
            meats = MultiSelectField(choices=PARTS)
        elif link == 1:
            buns = MultiSelectField(choices=PARTS)
        elif link == 2:
            condiments = MultiSelectField(choices=PARTS, blank=True)
        elif link == 3:
            salads = MultiSelectField(choices=PARTS, blank=True)
        elif link == 4:
            cheeses = MultiSelectField(choices=PARTS, blank=True)
        else:
            Exception("Indalid index for API part")






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
