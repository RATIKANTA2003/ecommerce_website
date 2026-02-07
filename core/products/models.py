from django.db import models
from django.contrib.auth.models import User

# --- PRODUCT MODEL ---
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('gadgets', 'Gadgets'),
        ('home', 'Home & Living'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='electronics'
    )
    stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name

# --- CART MODEL ---
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product_name}"

# --- ORDER MODEL ---
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    # --- USER PROFILE & ADDRESS ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    language = models.CharField(max_length=20, default='English')

    def __str__(self):
        return f"Profile for {self.user.username}"

class SavedAddress(models.Model):
    ADDRESS_TYPES = [('home', 'Home'), ('office', 'Office'), ('other', 'Other')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_addresses")
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home')
    full_address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_type.upper()} - {self.user.username}"
