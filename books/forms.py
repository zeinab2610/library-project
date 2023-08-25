from django import forms
from books.models import Book

class BooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
    publicationDate = forms.DateField(required=False)  # Set required to False
