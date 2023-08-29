from django.db import models
from email.policy import default
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    publication_date = models.DateField(null=True)
    category_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "books"
