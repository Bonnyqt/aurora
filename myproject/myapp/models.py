from django.db import models
import random
import string
from django.utils import timezone

class Table(models.Model):
    LOCATION_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor Patio'),
        ('private', 'Private Dining'),
        ('vip', 'VIP Section'),
    ]
    
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='indoor')
    is_available = models.BooleanField(default=True)
    x_position = models.IntegerField(default=100)
    y_position = models.IntegerField(default=100)
    
    def get_position_description(self):
        """Return description based on table position"""
        descriptions = {
            'indoor': {
                'near_bar': 'Close to bar counter',
                'near_kitchen': 'Near kitchen (faster service)',
                'center': 'Center of dining area',
                'near_window': 'Window view',
                'quiet': 'Quiet corner',
            },
            'outdoor': {
                'garden': 'Garden view',
                'patio': 'Outdoor patio',
                'fresh_air': 'Fresh air seating',
            },
            'private': {
                'intimate': 'Private intimate setting',
                'business': 'Perfect for business meetings',
                'family': 'Family gathering area',
            },
            'vip': {
                'exclusive': 'Exclusive VIP service',
                'premium': 'Premium location',
                'luxury': 'Luxury dining experience',
            }
        }
        
        # Simple logic based on position - you can make this more sophisticated
        if self.x_position > 600:  # Right side
            if self.location == 'indoor':
                return descriptions['indoor']['near_bar']
            elif self.location == 'vip':
                return descriptions['vip']['exclusive']
        elif self.x_position < 200:  # Left side
            return descriptions[self.location].get('near_kitchen', 'Cozy corner')
        elif self.y_position < 100:  # Top
            return descriptions[self.location].get('near_window', 'Great view')
        else:  # Center/bottom
            return descriptions[self.location].get('center', 'Prime location')
    
    def __str__(self):
        return f"Table {self.table_number} ({self.capacity} seats)"

    class Meta:
        ordering = ['table_number']


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    
    # Reference number generation
    reference_number = models.CharField(max_length=10, unique=True, blank=True)
    
    # Table and guest information
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    party_size = models.IntegerField()
    
    # Reservation details
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Generate reference number if not exists"""
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
        super().save(*args, **kwargs)
    
    def generate_reference_number(self):
        """Generate unique reference number"""
        while True:
            reference = 'AR' + ''.join(random.choices(string.digits, k=6))
            if not Reservation.objects.filter(reference_number=reference).exists():
                return reference
    
    def __str__(self):
        return f"Reservation {self.reference_number} - {self.guest_name} ({self.reservation_date})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    wants_promo_updates = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.email} - {'Active' if self.is_active else 'Inactive'}"
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'


# Optional: Contact form model for contact page submissions
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'