
from django.urls import include, path
from . import views

app_name='App_shop'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('product_details/<pk>/',views.ProductDetails.as_view(),name='product_details'),
    path('search/',views.search_function,name='search')
]
