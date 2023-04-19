from django import forms
from .models import Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('title', 'author', 'language', 'published_date', 'ISBN_number', 'pages_numbers', 'image_link')
