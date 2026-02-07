from django.urls import path
from .views import login_view, signup_view, account_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),
]
