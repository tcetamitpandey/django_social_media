# Generated by Django 5.0.3 on 2024-04-02 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('bio', models.TextField(blank=True)),
                ('profoleimg', models.ImageField(default='placeholder.jpg', upload_to='profile_images')),
                ('intrest', models.CharField(blank=True, choices=[('Music', 'Music'), ('Movies and TV Shows', 'Movies and TV Shows'), ('Sports', 'Sports'), ('Gaming', 'Gaming'), ('Fashion and Beauty', 'Fashion and Beauty'), ('Technology and Gadgets', 'Technology and Gadgets'), ('Travel and Adventure', 'Travel and Adventure'), ('Fitness and Wellness', 'Fitness and Wellness'), ('Art and Creativity', 'Art and Creativity'), ('Social Causes and Activism', 'Social Causes and Activism')], max_length=100)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
