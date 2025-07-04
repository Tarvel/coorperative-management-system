# Generated by Django 5.2.3 on 2025-06-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_loan_amount_alter_loan_balance_remaining_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="loan",
            name="balance_remaining",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
