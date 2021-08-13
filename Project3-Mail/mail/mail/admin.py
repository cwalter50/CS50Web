from django.contrib import admin

# Register your models here.

from .models import User, Email

# Register your models here.


admin.site.register(Email)
admin.site.register(User)

