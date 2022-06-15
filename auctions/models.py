from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=18, unique=True)
    class Meta:
        ordering = ('category',)

    def __str__(self):
        return f"{self.category}"


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented: {self.comment}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_bids")
    bid = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} with {self.bid}"


class Listing(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300, null=True)
    initial_bid = models.IntegerField()
    bid = models.ManyToManyField(Bid, blank=True, related_name="bids")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="similar_categories")
    created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings", null=True)
    saved_by = models.ManyToManyField(User, blank=True, related_name="saved_listings")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    image = models.CharField(max_length=200, default=None, blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name="listing_comments")

    def __str__(self):
        return f"{self.title} / {self.category} / {self.initial_bid}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    
    def __str__(self):
        return f"{self.user.username} added {self.listing.title}"



# FORMS:

class CommentsForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'initial_bid', 'category', 'image']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]
        labels = {"bid": ""}
        widgets = {
          'bid': forms.TextInput(attrs={'class': 'your-bid', 'placeholder': 'Type your bid $'})
        }



