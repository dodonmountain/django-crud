# Generated by Django 2.2.5 on 2019-09-23 06:05

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_thumbnail',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=''),
        ),
    ]