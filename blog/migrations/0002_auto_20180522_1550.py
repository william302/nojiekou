# Generated by Django 2.0.4 on 2018-05-22 07:50

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='user',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='avatar'),
        ),
    ]