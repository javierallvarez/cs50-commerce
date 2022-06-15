from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    act_listing = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": act_listing,
    })   


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })



def category(request, category_id):
    category = Category.objects.get(id=category_id)
    categories = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "categories": categories,
    })



def listing(request, listing_id): 
    listing = Listing.objects.get(id=listing_id)
    if listing.active is True:
        if request.method == "POST" and request.POST.get("close") or None:
            listing.active = False
            listing.save()
        return render(request,"auctions/listing.html", {
            "listing" : listing,
            "form": BidForm, 
            "comment_form": CommentsForm,  
    })
    else:    
        return render(request,"auctions/listing.html", {
            "listing" : listing,
            "form": BidForm,   
            "comment_form": CommentsForm,
    })
    


@login_required(login_url="/login")
def new_listing(request):
    if request.method =="POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html",{
                "form": form,
            })
    else:
        return render(request, "auctions/new_listing.html",{
                "form": ListingForm,
            })

 

@login_required(login_url="/login")
def open_watchlist(request):
    user = User.objects.get(username=request.user)
    watchlist = user.watchlist.all() 
    return render(request, "auctions/watchlist.html",{
                "user": user,
                "watchlists": watchlist,
            })



@login_required(login_url="/login")
def add_to_watchlist(request, listing_id):
    watchlist = Watchlist()
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(username=request.user)
    if user.watchlist.filter(listing=listing).exists():
        user.watchlist.filter(listing=listing).delete()
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "message": "Deleted from your Watchlist.",
            "added": False
        }) 
    else:    
        watchlist.user = user
        watchlist.listing = listing
        watchlist.save()
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "message": "Added to your Watchlist!",
            "watchlist": watchlist,
            "added": True,
        })  



def closed(request): 
    listing = Listing.objects.filter(active=False)
    return render(request, "auctions/closed.html",{
        "listings": listing,
    })



@login_required(login_url="/login")
def make_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = BidForm(request.POST)
    if form.is_valid():
        bid = float(request.POST["bid"])
        price = listing.initial_bid
        if bid > price:
            bid = form.save(commit=False)
            bid.user = request.user
            bid.save()
            listing.initial_bid = int(request.POST["bid"])
            listing.bid.add(bid)
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "form": BidForm,
                "confirmation": "Your bid was posted!",
           })
        else:
            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "form": BidForm,
                "error": "ERROR: Your bid is not enough",
           })
    return HttpResponseRedirect(reverse("listing", args=[listing_id])) 




@login_required(login_url="/login")
def post_comment (request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            return render(request, "auctions/listing.html", {
                "comment_form": comment_form,
                "listing": listing,
                "listing_id": listing.id,
            })
    return render(request, "auctions/listing.html", {
                "comment_form": comment_form,
                "listing": listing,
                "listing_id": listing.id,
                "all_comments": Comment.objects.order_by("-id")
            })
 