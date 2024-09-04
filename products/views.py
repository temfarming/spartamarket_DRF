from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Product

# Create your views here.
def product_list_html(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, "products/product_list.html", context)

def json_01(request):
    products = Product.objects.all()
    json_products = []

    for product in products:
        json_products.append(
            {            
            "title" : product.title,
            "content" : product.content,
            "created_at" : product.created_at,
            "updated_at" : product.updated_at,

            }
        )

    return JsonResponse(json_products, safe=False)

def json_02(request):
    products = Product.objects.all()
    res_data = serializers.serialize("json", products)
    return HttpResponse(res_data, content_type="application/json")