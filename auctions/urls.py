from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("create", views.new_listing, name="create"),
    path("<int:listing_id>", views.add_to_watchlist, name="watchlist"),
    path("watchlist/", views.open_watchlist, name="open_watchlist"),
    path("closed", views.closed, name="closed"),
    path("make_bid/<int:listing_id>", views.make_bid, name="make_bid"),
    path("<int:listing_id>/post_comment", views.post_comment, name="post_comment"),
]
