# Generated by Django 4.0.3 on 2023-08-26 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='category',
            new_name='category_id',
        ),
    ]
