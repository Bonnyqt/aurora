from django.contrib import admin
from .models import Table, Reservation, NewsletterSubscription, ContactMessage

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'location', 'is_available', 'x_position', 'y_position']
    list_filter = ['location', 'is_available', 'capacity']
    search_fields = ['table_number']
    list_editable = ['is_available', 'x_position', 'y_position']
    ordering = ['table_number']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'guest_name', 'email', 'table', 'reservation_date', 'reservation_time', 'party_size', 'status', 'created_at']
    list_filter = ['status', 'reservation_date', 'table__location', 'created_at']
    search_fields = ['reference_number', 'guest_name', 'email', 'mobile_number']
    readonly_fields = ['reference_number', 'created_at', 'updated_at']
    date_hierarchy = 'reservation_date'
    list_per_page = 25
    
    fieldsets = (
        ('Reservation Details', {
            'fields': ('reference_number', 'table', 'status')
        }),
        ('Guest Information', {
            'fields': ('guest_name', 'email', 'mobile_number', 'party_size')
        }),
        ('Booking Details', {
            'fields': ('reservation_date', 'reservation_time', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active', 'wants_promo_updates']
    list_filter = ['is_active', 'wants_promo_updates', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active', 'wants_promo_updates']
    date_hierarchy = 'subscribed_at'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )