# Generated by Django 4.2.4 on 2023-08-02 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=500)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
    ]
