# Generated by Django 3.2.1 on 2022-05-15 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
