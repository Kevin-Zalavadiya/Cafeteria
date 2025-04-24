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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import re


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
        username = request.POST.get('number', '').strip()
        password = request.POST.get('password', '')
        
        # Validate input
        if not username:
            messages.error(request, 'UID Number is required')
            return render(request, 'login.html')
        
        # Add validation for UID format (24MCA005)
        if not re.match(r'^\d{2}[A-Z]{3}\d{3}$', username):
            messages.error(request, 'UID Number should be in the format: 24MCA005')
            return render(request, 'login.html')
        
        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid UID Number or password')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        phone = request.POST.get('phone', '').strip()
        
        # Validate username (UID Number)
        if not username:
            messages.error(request, "UID Number is required.")
        # Changed validation to match format like 24MCA005
        elif not re.match(r'^\d{2}[A-Z]{3}\d{3}$', username):
            messages.error(request, "UID Number should be in the format: 24MCA005")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "This UID Number is already registered.")
        
        # Validate email
        if not email:
            messages.error(request, "Email is required.")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Please enter a valid email address.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")

        # Validate password
        if not password1:
            messages.error(request, "Password is required.")
        elif len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        
        # Validate password confirmation
        if not password2:
            messages.error(request, "Please confirm your password.")
        elif password1 != password2:
            messages.error(request, "Passwords don't match.")
        
        # Validate phone number
        if not phone:
            messages.error(request, "Phone number is required.")
        else:
            # Remove any non-digit characters
            phone_digits = re.sub(r'\D', '', phone)
            
            # Check if phone number has valid length
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                messages.error(request, "Phone number must be between 10 and 15 digits.")
        
        # If there are no error messages, create the user
        if not messages.get_messages(request):
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                
                # You can save the phone number to a profile model if needed
                # For example:
                # Profile.objects.create(user=user, phone=phone_digits)
                
                messages.success(request, "Registration successful! Please login with your credentials.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        
        # If there are errors, pass the submitted data back to the template
        context = {
            'username': username,
            'email': email,
            'phone': phone
        }
        return render(request, 'register.html', context)
    
    return render(request, 'register.html')

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
        email = request.POST.get('email')
        # Here you would implement the password reset logic
        # For example, send a reset link to the user's email
        # For now, we'll just render the template
        return render(request, 'forgot_password.html', {'email_sent': True})
    return render(request, 'forgot_password.html')

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