from django.db import models
from django.forms import ModelForm, Textarea


class Book(models.Model):
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)
  publicationDate = models.DateField(null=True)
  category = models.CharField(max_length=255)
class Meta:
    db_table = "books"
