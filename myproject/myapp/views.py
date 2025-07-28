from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Table, Reservation, NewsletterSubscription
import threading

# ...existing code...

def reservation_view(request):
    tables = Table.objects.filter(is_available=True)
    if request.method == 'POST':
        # Handle reservation form submission
        table_id = request.POST.get('table_id')
        guest_name = request.POST.get('guest_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        party_size = request.POST.get('party_size')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        special_requests = request.POST.get('special_requests', '')
        
        table = Table.objects.get(id=table_id)
        reservation = Reservation.objects.create(
            table=table,
            guest_name=guest_name,
            email=email,
            mobile_number=mobile_number,
            party_size=party_size,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            special_requests=special_requests
        )
        
        # Send confirmation email
        send_confirmation_email(reservation)
        
        return render(request, 'myapp/reservation_success.html', {
            'reservation': reservation
        })
    
    return render(request, 'myapp/reservation.html', {'tables': tables})

# REPLACE YOUR EXISTING send_confirmation_email WITH THIS:
def send_confirmation_email(reservation):
    subject = f'Reservation Confirmation - {reservation.reference_number}'
    message = f'''
Dear {reservation.guest_name},

Your reservation has been confirmed!

Reference Number: {reservation.reference_number}
Table: {reservation.table.table_number}
Date: {reservation.reservation_date}
Time: {reservation.reservation_time}
Party Size: {reservation.party_size}

Please arrive 15 minutes before your reservation time.

We look forward to serving you at Aurora Restaurant.

Best regards,
Aurora Restaurant Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.email],
            fail_silently=False,
        )
        print(f"Reservation confirmation email sent to {reservation.email}")
    except Exception as e:
        print(f"Failed to send reservation email: {e}")

# ADD THIS NEW FUNCTION (it doesn't exist in your current file):
def send_newsletter_confirmation_email(email):
    subject = 'Welcome to Aurora Restaurant Newsletter!'
    message = f'''
Dear Valued Guest,

You've been successfully subscribed to Aurora Restaurant newsletter!

You'll receive:
✓ Exclusive promotions and special offers
✓ News about new menu items and seasonal dishes
✓ Updates about special events and celebrations
✓ Early access to reservation slots for special occasions

Thank you for joining our community!

Best regards,
Aurora Restaurant Team

---
If you wish to unsubscribe, please contact us at info@aurora-restaurant.com
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"Newsletter confirmation email sent to {email}")
    except Exception as e:
        print(f"Failed to send newsletter email: {e}")

# REPLACE YOUR EXISTING newsletter_subscribe WITH THIS:
def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        wants_promo_updates = request.POST.get('promo_updates') == 'on'
        
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'wants_promo_updates': wants_promo_updates}
        )
        
        if created:
            # Send welcome email for new subscribers
            send_newsletter_confirmation_email(email)
            messages.success(request, 'Successfully subscribed to newsletter! Check your email for confirmation.')
        else:
            messages.info(request, 'You are already subscribed!')
            
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Main entry point (not currently used in the rest of the views)
def index(request):
    return render(request, 'myapp/index.html')

# Home page for Aurora (uses about.html template but acts as home)
def pacific2(request):
    return render(request, 'myapp/pacificstar/about.html', {'is_home': True})

# About page for Aurora
def about(request):
    return render(request, 'myapp/pacificstar/about.html', {'is_home': False})

# Aurora location view (standard page, no conditional logic)
def pacific(request):
    return render(request, 'myapp/pacificstar/aurora.html')

# Alternate Aurora page (maybe for different layout or version)
def pacific2(request):
    return render(request, 'myapp/pacificstar/aurora2.html')

# Bistro location view
def podium(request):
    return render(request, 'myapp/podium/bistro.html')

# Alternate Bistro page
def podium2(request):
    return render(request, 'myapp/podium/bistro2.html')

# REPLACE YOUR EXISTING reserve FUNCTION WITH THIS:
def reserve(request):
    tables = Table.objects.filter(is_available=True)
    
    print(f"DEBUG: Found {tables.count()} available tables")  # Debug line
    
    if request.method == 'POST':
        print(f"DEBUG: POST data received: {dict(request.POST)}")  # Debug line
        
        # Handle reservation form submission
        table_id = request.POST.get('table_id')
        guest_name = request.POST.get('guest_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        party_size = request.POST.get('party_size')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        special_requests = request.POST.get('special_requests', '')
        promo_updates = request.POST.get('promo_updates') == 'on'
        
        print(f"DEBUG: Table ID: {table_id}, Promo updates: {promo_updates}")  # Debug line
        
        try:
            if table_id:
                table = Table.objects.get(id=table_id)
                print(f"DEBUG: Found table: {table}")  # Debug line
                
                reservation = Reservation.objects.create(
                    table=table,
                    guest_name=guest_name,
                    email=email,
                    mobile_number=mobile_number,
                    party_size=party_size,
                    reservation_date=reservation_date,
                    reservation_time=reservation_time,
                    special_requests=special_requests
                )
                
                print(f"DEBUG: Reservation created: {reservation.reference_number}")  # Debug line
                
                # Handle newsletter subscription
                if promo_updates:
                    subscription, created = NewsletterSubscription.objects.get_or_create(
                        email=email,
                        defaults={'wants_promo_updates': True}
                    )
                    if created:
                        print(f"DEBUG: Newsletter subscription created for {email}")  # Debug line
                        send_newsletter_confirmation_email(email)
                    else:
                        print(f"DEBUG: User {email} already subscribed to newsletter")  # Debug line
                
                # Send reservation confirmation email
                send_confirmation_email(reservation)
                
                messages.success(request, f'Reservation confirmed! Reference: {reservation.reference_number}')
                return render(request, 'myapp/pacificstar/reservation_success.html', {
                    'reservation': reservation
                })
            else:
                # No table selected
                messages.error(request, 'Please select a table to make a reservation.')
                print("DEBUG: No table ID provided")  # Debug line
                return redirect('reserve')
            
        except Exception as e:
            print(f"DEBUG: Reservation error: {e}")  # Debug line
            messages.error(request, f'There was an error processing your reservation: {str(e)}')
            return redirect('reserve')
    
    return render(request, 'myapp/pacificstar/reserve.html', {
        'guest_range': range(1, 21),
        'tables': tables
    })

def contact(request):
    return render(request, 'myapp/pacificstar/contact.html')

def view_menu(request):
    return render(request, 'myapp/pacificstar/viewMenu.html')