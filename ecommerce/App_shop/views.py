from django.shortcuts import render
from django.views.generic import DetailView,ListView
from .models import Category,Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

class Home(ListView):
    paginate_by=4
    model=Product
    template_name='App_shop/home.html'

class ProductDetails(LoginRequiredMixin,DetailView):
    model=Product
    template_name="App_shop/product_details.html"

def search_function(request):
    query=request.GET['query']
    if len(query)>50:
        return Product.objects.none()
    else:
        product_title=Product.objects.filter(name__icontains=query)
    
    if product_title.count()==0:
        messages.info(request,f'No search result found!!!')
    return render(request,'App_shop/search.html',context={'product_title':product_title})
