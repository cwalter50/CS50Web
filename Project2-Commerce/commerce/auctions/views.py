from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all()
    message = ""
    if len(listings) == 0:
        message = "No Active Listings"
    return render(request, "auctions/index.html", {
        "listings": listings,
        "message": message
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

@login_required
def listing(request):
# def listing(request, listing_id):
    # listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        # "listing": listing
    })


@login_required
def createListing(request):
    # if user submitted the create listing form
    if request.method == "POST":
        # item is of type Listing (object)
        # item = Listing()
        # # assigning the data submitted via form to the object
        # item.owner = request.user
        # item.title = request.POST.get('title')
        # item.description = request.POST.get('description')
        # item.category = request.POST.get('category')
        # item.starting_bid = request.POST.get('starting_bid')
        # create a form using the ModelForm
        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            listings = Listing.objects.all()
            message = ""
            if len(listings) == 0:
                message = "No Active Listings"
            return render(request, "auctions/index.html", {
                "listings": listings,
                "message": message
            })
            # return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })
      