from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('category/<int:pk>/', views.category_books, name='category_books'),
    path('scan/', views.scan_isbn, name='scan_isbn'),
    
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path('upload/', views.upload_book, name='upload_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('approve-price/<int:pk>/', views.approve_price, name='approve_price'),
    
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # Auth & Profile
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('resend-otp/<str:flow>/', views.resend_otp, name='resend_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
