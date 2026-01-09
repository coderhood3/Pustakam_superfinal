from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Book, Order, OrderItem

@receiver(post_save, sender=Book)
def send_book_status_notification(sender, instance, created, **kwargs):
    """
    Sends email to the seller when book status changes.
    """
    subject = ""
    message = ""
    recipient_list = [instance.seller.email]
    
    if created:
        subject = f"Book Uploaded: {instance.title}"
        message = f"Hello {instance.seller.username},\n\nYour book '{instance.title}' has been uploaded successfully. It is currently Pending review. The Admin will set a price shortly."
    
    # Check if status has changed (simple check, for robust change detection we might need __init__ tracking, but this is okay for now if we rely on the save happening on status change)
    elif instance.status == 'Priced':
        subject = f"Valid Price Set: {instance.title}"
        message = f"Hello {instance.seller.username},\n\nGreat news! The Admin has set a price of ₹{instance.price} for your book '{instance.title}'.\nPlease log in to your dashboard and 'Approve' it to publish the book."

    elif instance.status == 'Published':
        subject = f"Book Published: {instance.title}"
        message = f"Hello {instance.seller.username},\n\nYour book '{instance.title}' is now LIVE and visible to buyers!"

    elif instance.status == 'Rejected':
        subject = f"Book Rejected: {instance.title}"
        message = f"Hello {instance.seller.username},\n\nUnfortunately, your book '{instance.title}' has been rejected by the admin."
    
    if subject and message:
        send_mail(subject, message, settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@pustakam.com', recipient_list)

@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    if created:
        # Email to Buyer
        subject_buyer = f"Order Confirmed #{instance.id}"
        message_buyer = f"Hello {instance.user.username},\n\nThank you for your order! Your order #{instance.id} for ₹{instance.total_amount} has been placed successfully."
        send_mail(subject_buyer, message_buyer, 'noreply@pustakam.com', [instance.user.email])

        # Email to Sellers (iterate over items)
        # Note: items are created AFTER order is created, so this signal might fire before items are added if not careful.
        # Better to do this in the view after creating items, OR use a separate signal or method.
        # But per the plan, let's keep it simple. If items aren't there yet, this won't work perfectly for sellers.
        # FIX: The view creates items after order. So `post_save` on Order `created=True` happens BEFORE items exist.
        # We should move the seller email logic to the Checkout View or a custom signal called "order_completed".
        # For now, I will let the View handle the seller notification to be safe, or just do buyer here.
        pass 

# Signal for manually triggering seller emails after items added
def send_seller_order_emails(order):
    seller_items = {}
    for item in order.items.all():
        seller = item.book.seller
        if seller not in seller_items:
            seller_items[seller] = []
        seller_items[seller].append(item)
    
    for seller, items in seller_items.items():
        subject = f"You made a sale! Order #{order.id}"
        item_list = "\n".join([f"- {item.book.title} (Qty: {item.quantity})" for item in items])
        message = f"Hello {seller.username},\n\nGood news! You have sold the following books:\n\n{item_list}\n\nPlease prepare them for shipping."
        send_mail(subject, message, 'noreply@pustakam.com', [seller.email])
