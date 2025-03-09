from django.urls import path
from . import views
from .views import contact, subscribe_newsletter, forgot_password, food_items

urlpatterns = [
    # Add your URL patterns here
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),  # Placeholder
    path('feature/', views.feature, name='feature'),  # Placeholder
    path('team/', views.team, name='team'),  # Placeholder
    path('menu/', views.menu, name='menu'),  # Placeholder
    path('contact/', contact, name='contact'),
    path('forgot-password/', forgot_password, name='forgot_password'), 
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('cart/', food_items, name='cart'),
    path('invoice/', views.invoice_view, name='invoice'),
    
]
