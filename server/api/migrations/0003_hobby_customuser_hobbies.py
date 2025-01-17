# Generated by Django 5.1.4 on 2025-01-17 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_friend_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'hobbies',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='hobbies',
            field=models.ManyToManyField(blank=True, related_name='users', to='api.hobby'),
        ),
    ]
