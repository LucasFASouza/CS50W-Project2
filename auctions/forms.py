from django import forms
from .models import Listing, Biding


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'photo_url', 'initial_bid']
