from django import forms
from books.models import Book, Category
from random import random
from secrets import choice
from sys import prefix
from unicodedata import category
from numpy import require
from django.core.exceptions import ValidationError 

class BooksForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
    publicationDate = forms.DateField(required=False)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        existing_book = Book.objects.filter(name=name).exclude(pk=self.instance.pk)
        if existing_book.exists():
            raise ValidationError("A book with this name already exists.")
        return name

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.Textarea()

    class Meta:
        model = Category
        fields = "__all__"
        
    def clean_name(self):
        name = self.cleaned_data['name']
        existing_category = Category.objects.filter(name=name).exclude(pk=self.instance.pk)
        if existing_category.exists():
            raise ValidationError("A category with this name already exists.")
        return name