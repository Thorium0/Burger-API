from django.urls import path
from . import views

urlpatterns = [
    path('', views.burgerList, name='burgers'),
    path('add/', views.addBurger, name='addBurger'),
    path('<id>/', views.displayBurger, name='displayBurger'),
    path('<id>/delete', views.delBurger, name='delBurger'),
    path('<id>/edit', views.editBurger, name='editBurger'),
]
