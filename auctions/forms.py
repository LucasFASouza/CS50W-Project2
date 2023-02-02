from django import forms
from .models import Listing, Biding, Comment


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'photo_url', 'initial_bid']


class NewBid(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.buyer = kwargs.pop('buyer')

        super(NewBid, self).__init__(*args, **kwargs)

    def clean(self):
        value = self.cleaned_data['value']
        if value <= self.item.price:
            raise forms.ValidationError("Your bid is lower than current price")

        if self.buyer == self.item.seller:
            raise forms.ValidationError("You can't place bids in your own products")

        return self.cleaned_data

    class Meta:
        model = Biding
        fields = ['value']


class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

