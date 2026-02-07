from django.contrib import admin
from django.utils.html import format_html
from .models import Product, CartItem, Order, Profile, SavedAddress

# --- CUSTOMIZE ADMIN HEADERS ---
admin.site.site_header = "HYPER STORE | Command Center"
admin.site.site_title = "Hyper Admin Portal"
admin.site.index_title = "E-commerce Management Engine"

# --- PRODUCT MANAGEMENT ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Displays thumbnails and stock info in the list
    list_display = ('get_image', 'name', 'category', 'price', 'id')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('price',) # Quick price updates from the main list

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; border: 1px solid #00c9ff;" />', obj.image.url)
        return "No Image"
    get_image.short_description = 'Preview'

# --- ORDER & REVENUE TRACKING ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at', 'is_completed')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('user__username', 'address', 'city')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',) # Newest orders at the top

# --- USER IDENTITY & ADDRESSES ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_avatar', 'user', 'mobile', 'language')
    search_fields = ('user__username', 'mobile')

    def get_avatar(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.profile_pic.url)
        return "No Photo"
    get_avatar.short_description = 'Avatar'

@admin.register(SavedAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'city', 'zip_code')
    list_filter = ('address_type', 'city')
    search_fields = ('user__username', 'full_address')

# --- CART UTILITIES ---
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'quantity', 'price')
    search_fields = ('user__username', 'product_name')