from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import Book, Category, Cart, CartItem, Order, OrderItem, Review, Wishlist, BookImage
from .forms import RegistrationForm, BookForm, ReviewForm
from .signals import send_seller_order_emails

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate until OTP verification
            user.save()
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store in session
            request.session['pre_otp_user_id'] = user.id
            request.session['otp'] = otp
            
            # Send Email
            send_mail(
                'Verify Your Registration - Pustakam',
                f'Hello {user.username},\n\nYour OTP for registration is: {otp}\n\nVerify this code to activate your account.',
                settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@pustakam.com',
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Account created! OTP sent to {user.email}. Please verify to activate.')
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'books/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
             login(request, user)
             messages.success(request, f'Welcome back, {user.username}!')
             return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'books/login.html')

def verify_otp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if entered_otp == session_otp:
            # Success
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            
            # Activate User
            user.is_active = True
            user.save()
            
            # Specify backend explicitly to avoid "User has no backend" error
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            # Clear session
            del request.session['pre_otp_user_id']
            del request.session['otp']
                
            messages.success(request, 'Registration verified! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'books/verify_otp.html')

def about(request):
    return render(request, 'books/about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Message sent! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'books/contact.html')

def home(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    
    if query:
        # If searching, show matching books
        featured_books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn=query),
            status='Published'
        )
        recent_books = Book.objects.none() # Hide recent section slightly or just show results
        search_mode = True
    else:
        # Default view
        featured_books = Book.objects.filter(status='Published', condition='New')[:4]
        recent_books = Book.objects.filter(status='Published').order_by('-created_at')[:8]
        search_mode = False

    return render(request, 'books/home.html', {
        'categories': categories, 
        'featured_books': featured_books,
        'recent_books': recent_books,
        'search_query': query,
        'search_mode': search_mode
    })

def category_books(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category, status='Published')
    return render(request, 'books/category_books.html', {'category': category, 'books': books})

def scan_isbn(request):
    return render(request, 'books/scan_isbn.html')

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added!')
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    
    images = book.images.all()
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews, 'form': form, 'images': images})

@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.status = 'Pending' # Ensure pending
            book.save()
            messages.success(request, 'Book uploaded successfully! Admin will check and set the price.')
            return redirect('my_books')
    else:
        form = BookForm()
    return render(request, 'books/upload.html', {'form': form})

@login_required
def my_books(request):
    books = Book.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'books/my_books.html', {'books': books})

@login_required
def approve_price(request, pk):
    book = get_object_or_404(Book, pk=pk, seller=request.user)
    if book.status == 'Priced':
        book.status = 'Published'
        book.save()
        messages.success(request, f'Price approved! {book.title} is now LIVE.')
    return redirect('my_books')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'books/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            total_amount=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        
        # Initial email to buyer (via signal) and Manual trigger for sellers
        send_seller_order_emails(order) # Call the helper from signals.py

        cart.items.all().delete()
        messages.success(request, 'Order placed successfully! Check your email.')
        return redirect('home') # Or order tracking page
    return render(request, 'books/checkout.html', {'cart': cart})

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'books/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    messages.success(request, 'Added to wishlist!')
    return redirect('wishlist')
