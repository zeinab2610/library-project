# Generated by Django 4.0.3 on 2023-08-26 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_category_delete_flag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='date_added',
        ),
    ]
