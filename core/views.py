from django.shortcuts import render, redirect
from django.contrib import messages
from seller.models import Product, ProductVariant
from customer.models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def buy_again(request):
    return render(request, 'buyagain.html')

def login_view(request):
    return render(request, 'login.html')

# def main_home(request):
#     # Get approved and active products with their first variant's price
#     products = Product.objects.filter(
#         approval_status='APPROVED',
#         is_active=True
#     ).select_related('subcategory', 'seller').prefetch_related('variants')[:12]
    
#     return render(request, 'mainhome.html', {'products': products})

def order_details(request):
    return render(request, 'orderdetails.html')


def product_single(request, slug):
    product = get_object_or_404(ProductVariant.objects.select_related('product').prefetch_related('images'), slug=slug)
    
    cart_count = 0
    is_in_cart = False
    all_wishlists = []
    active_wishlist_id = None
    active_wishlist = None
    is_in_wishlist = False
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = CartItem.objects.filter(cart=cart).count()
            is_in_cart = CartItem.objects.filter(cart=cart, variant=product).exists()
        except Cart.DoesNotExist:
            cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = CartItem.objects.filter(cart=cart).count()
        except Cart.DoesNotExist:
            cart_count = 0
        
        # Get all user's wishlists
        all_wishlists = Wishlist.objects.filter(user=request.user).order_by('-created_at')
        
        # Get active wishlist from session or use default
        active_wishlist_id = request.session.get('active_wishlist_id')
        
        if active_wishlist_id:
            # Verify the wishlist belongs to this user
            active_wishlist = all_wishlists.filter(id=active_wishlist_id).first()
            if not active_wishlist:
                # Invalid wishlist ID, use default
                active_wishlist = all_wishlists.filter(wishlist_name=request.user.username).first()
        else:
            # Default to username-based wishlist
            active_wishlist = all_wishlists.filter(wishlist_name=request.user.username).first()
        
        # If still no active wishlist, use the first one
        if not active_wishlist and all_wishlists.exists():
            active_wishlist = all_wishlists.first()
            request.session['active_wishlist_id'] = str(active_wishlist.id)
        
        # Check if product is in active wishlist
        if active_wishlist:
            active_wishlist_id = active_wishlist.id
            is_in_wishlist = WishlistItem.objects.filter(
                wishlist=active_wishlist, 
                variant=product
            ).exists()
    
    return render(request, 'core-templates/productsingle.html', {
        "data": product, 
        'cart_count': cart_count,
        'all_wishlists': all_wishlists,
        'active_wishlist_id': active_wishlist_id,
        'active_wishlist_name': active_wishlist.wishlist_name if active_wishlist else request.user.username,
        'is_in_wishlist': is_in_wishlist,
        'is_in_cart': is_in_cart
    })

@login_required
def single_product_checkout(request, slug):
    """
    Buy Now from single product - clear cart and add single item with POST quantity
    """
    variant = get_object_or_404(ProductVariant.objects.select_related('product'), slug=slug)
    
    if variant.stock_quantity <= 0:
        messages.error(request, 'Item out of stock.')
        return redirect('product_single', slug=slug)
    
    # Get quantity from POST, validate and default to 1
    quantity = 1
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity', 1))
            quantity = max(1, min(qty, variant.stock_quantity))
        except (ValueError, TypeError):
            quantity = 1
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Clear existing items for Buy Now (replace cart)
    cart.items.all().delete()
    
    # Add single item with quantity
    CartItem.objects.create(
        cart=cart,
        variant=variant,
        quantity=quantity,
        price_at_time=variant.selling_price
    )
    
    # Set session flag for single checkout detection
    request.session['single_checkout'] = True
    request.session['single_product_slug'] = slug
    
    messages.success(request, f'{quantity} x {variant.product.name} added for quick checkout!')
    return redirect('checkout')
