from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import User, Listing, Bid, Comment
from .forms import CommentForm, ListingForm, BidForm


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
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            listing.comments.add(comment)
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            return render(request, "auctions/comment.html", {
                "form": form,
                "listing_id": listing.id
            })
    else:
        return render(request, "auctions/comment.html", {
            "form": CommentForm(),
            "listing_id": listing.id
        })

def watchlist(request):
    return(render(request, "auctions/watchlist.html"))



@login_required
# def listing(request):
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if request.POST.get("button") == "Place Bid":
            form = BidForm(request.POST)
            if form.is_valid():
                # clean up this
                bid = form.save(commit=False)
                bid.user = request.user
                bid.save()
                # make sure bid is larger than the current max and above starting bid

                # maxBid = Bid()
                # if len(listing.bids.all()) > 0:
                # maxBid = max(listing.bids.all(), key=lambda b:b.price)
                # maxBid = getMaxBid(listing_id)
                message = ""
                if bid.price > listing.current_price and bid.price > listing.starting_bid:
                    listing.bids.add(bid)
                    listing.current_price = bid.price
                    listing.save()
                    message = f"added a new bid {bid}"
                else:
                    message = "Bid is not above the current max bid or starting bid."
                
                # listing.price = price
                
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": BidForm(),
                    "message": message
                })
        if not listing.closed:
            if request.POST.get("button") == "Close": 
                listing.closed = True
                listing.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Just closed the listing"
                })
            else:
                price = float(request.POST["price"])
                bids = listing.bids.all()
                if request.user.username != listing.owner.username: # only let those who dont own the listing be able to bid
                    if price <= listing.starting_bid:
                        return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "form": BidForm(),
                            "message": "Error! Invalid bid amount!"
                        })
                    form = BidForm(request.POST)
                    if form.is_valid():
                        # clean up this
                        bid = form.save(commit=False)
                        bid.user = request.user
                        bid.save()
                        listing.bids.add(bid)
                        listing.price = price
                        listing.save()
                    else:
                        return render(request, 'auctions/listing.html', {
                            "listing": listing,
                            "form": form,
                            "message": "Created HTML in the middle"
                        })

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(), 
        "message": "Created HTML at the very bottom"
    })

@login_required
def show_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if not listing.closed:
            if request.POST.get("button") == "Close": 
                listing.closed = True
                listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing
        # "user": request.user
    })
    # if request.method == "POST":
    #     user = User.objects.get(username=request.user)
    #     if request.POST.get("button") == "Watchlist": 
    #         if not user.watchlist.filter(listing= listing):
    #             watchlist = Watchlist()
    #             watchlist.user = user
    #             watchlist.listing = listing
    #             watchlist.save()
    #         else:
    #             user.watchlist.filter(listing=listing).delete()
    #         return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    #     if not listing.closed:
    #         if request.POST.get("button") == "Close": 
    #             listing.closed = True
    #             listing.save()
    #         else:
    #             price = float(request.POST["price"])
    #             bids = listing.bids.all()
    #             if user.username != listing.owner.username: # only let those who dont own the listing be able to bid
    #                 if price <= listing.price:
    #                     return render(request, "auctions/listing.html", {
    #                         "listing": listing,
    #                         "form": BidForm(),
    #                         "message": "Error! Invalid bid amount!"
    #                     })
    #                 form = BidForm(request.POST)
    #                 if form.is_valid():
    #                     # clean up this
    #                     bid = form.save(commit=False)
    #                     bid.user = user
    #                     bid.save()
    #                     listing.bids.add(bid)
    #                     listing.price = price
    #                     listing.save()
    #                 else:
    #                     return render(request, 'auctions/listing.html', {
    #                         "form": form
    #                     })
    #     return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    # else:
    #     return render(request, "auctions/listing.html", {
    #         "listing": listing,
    #         "form": BidForm(),
    #         "message": ""
    #     })


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
      
