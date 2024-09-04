from django.shortcuts import render
from .models import Product

# Create your views here.
def product_list_html(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, "products/product_list.html", context)