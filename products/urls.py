from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("html/", views.product_list_html, name = "product_list_html"),
    path("json-01", views.json_01, name="json_01"),
    
    
]
