# Generated by Django 3.0.6 on 2020-07-31 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200726_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='{static "/images/profile.jpeg"}', null=True, upload_to=''),
        ),
    ]
