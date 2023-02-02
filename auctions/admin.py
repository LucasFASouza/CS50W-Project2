from django.contrib import admin

from .models import User, Listing, Biding, Comment

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Biding)
admin.site.register(Comment)
