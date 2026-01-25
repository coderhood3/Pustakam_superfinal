from .models import Cart, Wishlist

def badge_counts(request):
    if request.user.is_authenticated:
        # Get Cart Count
        cart = Cart.objects.filter(user=request.user).first()
        cart_count = cart.items.count() if cart else 0
        
        # Get Wishlist Count
        wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist_count = wishlist.books.count() if wishlist else 0
        
        return {
            'cart_count': cart_count,
            'wishlist_count': wishlist_count
        }
    return {
        'cart_count': 0,
        'wishlist_count': 0
    }
