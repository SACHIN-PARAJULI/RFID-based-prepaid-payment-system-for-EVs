# Generated by Django 3.2.1 on 2022-05-11 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='contact',
            field=models.CharField(default=9800000000, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='account',
            name='card_uid',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='balance_after_transaction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12),
        ),
    ]
