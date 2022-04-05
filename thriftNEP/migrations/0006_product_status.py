# Generated by Django 4.0.1 on 2022-02-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thriftNEP', '0005_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('On Sale', 'On Sale'), ('Sold', 'Sold'), ('Disabled', 'Disabled')], default='On Sale', max_length=20),
            preserve_default=False,
        ),
    ]
