# Generated by Django 4.2.9 on 2024-01-16 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0009_rename_subjectevaluationitems_subjectevaluationitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="subjectevaluationitem",
            name="subject",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="models.subject",
            ),
        ),
    ]
