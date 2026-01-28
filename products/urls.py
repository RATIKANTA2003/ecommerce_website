from django.urls import path
from . import views

urlpatterns = [
    # Main Feed & Detail
    path('', views.product_list, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Cart Operations
    path('cart/', views.cart_view, name='cart_page'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-item/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout & Deployment
    path('place-order/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('invoice/<int:order_id>/', views.order_invoice, name='order_invoice'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.update_profile, name='update_profile'),
]