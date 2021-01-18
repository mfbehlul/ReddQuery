# Generated by Django 3.1.4 on 2021-01-09 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1200)),
                ('upvote', models.CharField(max_length=16)),
                ('downvote', models.CharField(max_length=16)),
                ('score', models.CharField(max_length=16)),
                ('author', models.CharField(max_length=1200)),
                ('subreddit', models.CharField(max_length=1200)),
            ],
        ),
    ]
