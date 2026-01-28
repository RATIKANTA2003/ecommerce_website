from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from .models import Product, CartItem, Order, Profile, SavedAddress
from django.contrib.auth.models import User

# --- 1. PRODUCT & LISTING VIEWS ---

def product_list(request):
    query = request.GET.get('search')
    category_filter = request.GET.get('category')
    products = Product.objects.all()
    top_sellers = Product.objects.all().order_by('-price')[:3]

    if category_filter and category_filter != 'all':
        products = products.filter(category=category_filter)
    if query:
        products = products.filter(name__icontains=query)

    cart_count = 0
    user_location = "Bhubaneswar, Odisha"
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
        # Dynamic location check
        default_addr = SavedAddress.objects.filter(user=request.user).first()
        if default_addr:
            user_location = f"{default_addr.city}, Odisha"

    return render(request, 'products/product_list.html', {
        'products': products, 
        'top_sellers': top_sellers,
        'user_location': user_location, 
        'cart_count': cart_count,
        'user': request.user
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    return render(request, 'products/product_detail.html', {
        'product': product, 
        'cart_count': cart_count
    })

# --- 2. CART & PURCHASE LOGIC ---

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.price for item in items)
    cart_count = items.count()
    return render(request, 'products/cart.html', {
        'items': items, 
        'total': total, 
        'cart_count': cart_count
    })

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            price = float(request.POST.get('price'))
            qty = int(request.POST.get('quantity', 1))
            CartItem.objects.create(
                user=request.user, product_name=name, 
                price=price * qty, quantity=qty
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_page')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart_page')
        
        total = sum(item.price for item in cart_items)
        with transaction.atomic():
            new_order = Order.objects.create(
                user=request.user,
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                zip_code=request.POST.get('zip'),
                total_price=total,
                is_completed=True
            )
            cart_items.delete()
        return redirect('order_success', order_id=new_order.id)
    return redirect('cart_page')

# --- 3. INVOICE & SUCCESS ---

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/success.html', {'order': order})

@login_required
def order_invoice(request, order_id):
    """This function fixes the most recent AttributeError"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/invoice.html', {'order': order})

# --- 4. PROFILE & ADDRESS MANAGEMENT ---

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    addresses = SavedAddress.objects.filter(user=request.user)
    return render(request, 'accounts/account.html', {
        'profile': profile,
        'addresses': addresses
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        user.save()
        profile.mobile = request.POST.get('mobile')
        profile.language = request.POST.get('language')
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        messages.success(request, "Hyper Profile Updated!")
    return redirect('profile_view')

@login_required
def add_address(request):
    if request.method == 'POST':
        SavedAddress.objects.create(
            user=request.user,
            address_type=request.POST.get('address_type'),
            full_address=request.POST.get('full_address'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('zip_code')
        )
    return redirect('profile_view')

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(SavedAddress, id=address_id, user=request.user)
    address.delete()
    return redirect('profile_view')