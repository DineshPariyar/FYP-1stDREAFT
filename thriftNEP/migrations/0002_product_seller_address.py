# Generated by Django 4.0.1 on 2022-02-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thriftNEP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]