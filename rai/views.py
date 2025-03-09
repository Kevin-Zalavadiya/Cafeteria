import pdfkit
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Contact, NewsletterSubscriber, FoodItem
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('index')

def finaltest(request):
    return render(request, 'finaltest.html')
  
  
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                subscriber = NewsletterSubscriber(email=email)
                subscriber.save()
                return render(request, 'index.html', {'success': True})
            except IntegrityError:
                return render(request, 'index.html', {'error': 'Email already subscribed.'})
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('number')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # Update the profile with phone number
            user.profile.phone = phone
            user.profile.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except Exception as e:
            print(f"Registration error: {str(e)}")
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'register.html')

    return render(request, 'register.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(f"Received data - Name: {name}, Email: {email}, Subject: {subject}, Message: {message}")

        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()


        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                subscriber = NewsletterSubscriber(email=email)
                subscriber.save()
                return render(request, 'index.html', {'success': True})
            except IntegrityError:
                return render(request, 'index.html', {'error': 'Email already subscribed.'})
    return render(request, 'index.html')

def feature(request):
    return render(request, 'feature.html')

def team(request):
    return render(request, 'team.html')

def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html')

def forgot_password(request):
    if request.method == 'POST':
        pass  
    return render(request, 'forgot_password.html')  # Ensure you have this template

@login_required
def food_items(request):
    """
    View function for displaying food items on the menu page.

    Parameters
    ----------
    request : HttpRequest
        The request object passed in by Django.

    Returns
    -------
    HttpResponse
        The rendered HTML page with the food items.

    Notes
    -----
    This view function retrieves all food items from the database and passes
    them to the template in the context as 'items'. The rendered page displays
    the food items with their respective names, prices, and images.
    """
    items = FoodItem.objects.all()
    return render(request, 'finaltest.html', {'items': items})


def invoice_view(request):
    """
    View function for displaying the invoice.
    
    This function renders the invoice.html template, which will display the total
    price passed from finaltest.html via localStorage on the client side.
    
    Parameters
    ----------
    request : HttpRequest
        The request object passed in by Django.
        
    Returns
    -------
    HttpResponse
        The rendered invoice.html template.
    """
    return render(request, 'invoice.html')  
