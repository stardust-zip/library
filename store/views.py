from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Category
from .cart import Cart


# Create your views here.
def home(request):
    categories = Category.objects.all()

    query = request.GET.get("q")

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    context = {"products": products, "categories": categories}

    return render(request, "store/home.html", context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {"product": product}

    return render(request, "store/product_detail.html", context)


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)

    quantity = int(request.POST.get("quantity", 1))
    cart.add(product=product, quantity=quantity)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "store/cart_detail.html", {"cart": cart})


@require_POST
def cart_update(request, pk):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity"))

    if quantity > 0:
        cart.update(pk, quantity)
    else:
        cart.remove(pk)
    return redirect("cart_detail")


def cart_remove(request, pk):
    cart = Cart(request)
    cart.remove(pk)
    return redirect("cart_detail")
