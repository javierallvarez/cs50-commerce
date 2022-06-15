from django.contrib import admin
from .models import Category, Listing, Comment, User, Watchlist

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Watchlist)