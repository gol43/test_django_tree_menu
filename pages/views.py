from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


def home(request):
    return render(request, 'pages/home.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


class ProductListView(ListView):
    model = Product
    template_name = 'pages/products.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)