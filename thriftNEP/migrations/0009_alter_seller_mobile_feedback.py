# Generated by Django 4.0.2 on 2022-05-07 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thriftNEP', '0008_alter_admin_mobile_productimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='mobile',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=200, null=True)),
                ('help_description', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thriftNEP.seller')),
            ],
        ),
    ]