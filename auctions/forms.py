from django import forms


class NewListing(forms.Form):
    title = forms.CharField(label="Listing Title", max_length=64)
    description = forms.CharField(
        label="Listing Description",
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 1})
    )
    initial_bid = forms.DecimalField(label="Initial Bid", max_digits=6, decimal_places=2)
    photo_url = forms.URLField(label="Photo URL")

    CATEGORIES_CHOICES = (
        ('Fashion', 'Fashion'),
        ('Home', 'Home'),
        ('Electronics', 'Electronics'),
        ('Toys', 'Toys'),
        ('Other', 'Other')
    )

    category = forms.ChoiceField(label="Category", choices=CATEGORIES_CHOICES)
