from django import forms
from .models import Books


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)