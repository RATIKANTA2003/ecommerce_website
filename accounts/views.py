from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  # Required to create new users

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        cp = request.POST.get('confirm_password')

        # 1. Check if passwords match
        if p != cp:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/signup.html')

        # 2. Check if username already exists
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'accounts/signup.html')

        # 3. Create the User
        user = User.objects.create_user(username=u, email=e, password=p)
        messages.success(request, 'Account initialized successfully! Please log in.')
        return redirect('login')

    return render(request, 'accounts/signup.html')

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/account.html')

def logout_view(request):
    logout(request)
    return redirect('products')