# Generated by Django 5.2.1 on 2025-05-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('contenu', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('publie', models.BooleanField(default=False)),
            ],
        ),
    ]
