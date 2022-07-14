from django import forms


class LinkForm(forms.Form):
    user_link = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control btn-block", 'placeholder': 'Enter your link'}))
