from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from distutils.command.upload import upload
from email.policy import default
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)
  publicationDate = models.DateField(null=True)
  category = models.CharField(max_length=255)
class Meta:
    db_table = "books"

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now = True)

    class Meta:
          db_table = "categories"
    def __str__(self):
        return str(f"{self.name}")
