from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Bid(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} put a bid in for {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    title = models.CharField(max_length=64, default="")
    comment = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"

class Listing(models.Model):
    item = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name="owner")
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    image = models.ImageField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.item}: is {self.price} and is being sold by {self.owner}"