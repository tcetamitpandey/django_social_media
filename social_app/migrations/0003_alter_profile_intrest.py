# Generated by Django 5.0.3 on 2024-04-02 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0002_interest_remove_profile_intrest_profile_intrest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='intrest',
            field=models.ManyToManyField(choices=[('None', ''), ('Music', 'Music'), ('Movies and TV Shows', 'Movies and TV Shows'), ('Sports', 'Sports'), ('Gaming', 'Gaming'), ('Fashion and Beauty', 'Fashion and Beauty'), ('Technology and Gadgets', 'Technology and Gadgets'), ('Travel and Adventure', 'Travel and Adventure'), ('Fitness and Wellness', 'Fitness and Wellness'), ('Art and Creativity', 'Art and Creativity'), ('Social Causes and Activism', 'Social Causes and Activism')], default='', to='social_app.interest'),
        ),
    ]
