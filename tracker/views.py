from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from .tasks import scrape_product_price

@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            # Trigger the first scrape immediately
            scrape_product_price.delay(product.id)
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'tracker/product_list.html', {'products': products, 'form': form})


@login_required
def product_delete(request, product_id):
    # This is a secure way to get the product. It ensures the product exists
    # AND that it belongs to the currently logged-in user.
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    # Redirect if someone tries to access this URL with a GET request
    return redirect('product_list')