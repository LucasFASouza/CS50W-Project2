from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing
from . import forms


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def listing(request, listing_id):
    auction = Listing.objects.get(id=listing_id)
    bidings = auction.bidings.all()

    return render(request, "auctions/listing.html", {
        "listing": auction,
        "bidings": bidings,
        "form": forms.NewBid(item=auction)
    })


@login_required
def add_listing(request):
    if request.method == "POST":
        form = forms.NewListing(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.seller = request.user
            obj.price = obj.initial_bid
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = forms.NewListing()

    return render(request, "auctions/add.html", {
        "form": form
    })


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        item = Listing.objects.get(id=listing_id)
        buyer = request.user
        form = forms.NewBid(request.POST, item=item, buyer=buyer)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.buyer = buyer
            obj.item = item
            obj.save()

            item.price = obj.value
            item.save()

            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        else:
            return render(request, "auctions/listing.html", {
                "listing": item,
                "bidings": item.bidings.all(),
                "form": form
            })