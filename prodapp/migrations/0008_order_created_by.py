# Generated by Django 5.0.6 on 2024-07-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodapp', '0007_rename_creative_date_order_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_by',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
    ]
