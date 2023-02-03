from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/close", views.close_auction, name="close"),
    path("<int:listing_id>/favorite", views.favorite, name="favorite"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
]
