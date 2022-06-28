from django.urls import path,include
from . import views

app_name='App_payment'

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('pay/',views.payment,name='payment'),
    path('status/',views.complete,name='complete'),
    path('purchase/<val_id>/<tran_id>/',views.purchase,name='purchase'),
    path('order/',views.order,name='order')
]
