from django.contrib import admin
from django.http import HttpResponse
from .models import *
from .models import Profile, Contact, NewsletterSubscriber, FoodItem
from django.shortcuts import redirect
import pdfkit
from . import views


class PROFILE(admin.ModelAdmin):
    list_display = ["user","phone","address","created_at","updated_at"]
admin.site.register(Profile,PROFILE)

class CONTACT(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "message", "created_at"]
admin.site.register(Contact, CONTACT)

class NEWSLETTER(admin.ModelAdmin):
    list_display = ["email", "created_at"]
admin.site.register(NewsletterSubscriber, NEWSLETTER)



class FOOD(admin.ModelAdmin):
    list_display = ["name", "price", "description", "image"]
admin.site.register(FoodItem,FOOD)

class ORDER(admin.ModelAdmin):
    list_display = ["id", "total_amount", "created_at"]  # Ensure 'items' is not included
admin.site.register(Order,ORDER)
