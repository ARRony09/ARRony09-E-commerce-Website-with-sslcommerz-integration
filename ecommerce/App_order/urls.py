
from django.urls import path,include
from . import views

app_name='App_order'
urlpatterns = [
    path('add/<pk>/',views.add_to_cart,name='add'),
    path('remove/<pk>/',views.remove_from_cart,name='remove'),
    path('cart/',views.view_cart,name='cart'),
    path('increase/<pk>/',views.increase_cart,name='increase_cart'),
    path('decrease/<pk>/',views.decrease_cart,name='decrease_cart'),
    
]
