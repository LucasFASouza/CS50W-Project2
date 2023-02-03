from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Comment
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
    comments = auction.comments.all()
    user = request.user

    bid_form = forms.NewBid(item=auction, buyer=user)
    comment_form = forms.NewComment()

    try:
        last_bid = bidings.latest('value')
    except:
        last_bid = None

    if request.method == "POST" and user.is_authenticated:
        if 'bid' in request.POST:
            bid_form = forms.NewBid(request.POST, item=auction, buyer=user)

            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.buyer = user
                bid.item = auction
                bid.save()

                auction.price = bid.value
                auction.buyer = user
                auction.save()

                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

        if 'comment' in request.POST:
            comment_form = forms.NewComment(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = user
                comment.auction = auction
                comment.save()

                return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

    return render(request, "auctions/listing.html", {
        "listing": auction,
        "bidings": bidings,
        "last_bid": last_bid,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
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
def close_auction(request, listing_id):
    auction = Listing.objects.get(id=listing_id)
    user = request.user

    if user.is_authenticated and auction.seller == user:
        auction.active = False
        auction.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
