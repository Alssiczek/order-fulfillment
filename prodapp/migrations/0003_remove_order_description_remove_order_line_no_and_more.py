# Generated by Django 5.0.6 on 2024-07-15 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodapp', '0002_order_creative_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='line_no',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_no',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seq_no',
        ),
        migrations.AddField(
            model_name='order',
            name='serial_number',
            field=models.CharField(default='UKNOWN', max_length=100),
            preserve_default=False,
        ),
    ]
