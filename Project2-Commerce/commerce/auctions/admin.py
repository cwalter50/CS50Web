from django.contrib import admin

from .models import Bid, Comment, Listing, User, Watchlist

# Register your models here.

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)
# Register your models here.
# class FlightAdmin(admin.ModelAdmin):
#     list_display = ("id", "origin", "destination", "duration")

# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)

# admin.site.register(Airport)
# admin.site.register(Flight, FlightAdmin)
# admin.site.register(Passenger, PassengerAdmin)
