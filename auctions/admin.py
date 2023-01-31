from django.contrib import admin

from .models import User, Listing, Biding

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Biding)
