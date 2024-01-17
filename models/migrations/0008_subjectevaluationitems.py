# Generated by Django 4.2.9 on 2024-01-16 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0007_curriculum_eval_percentage_curriculum_eval_status_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubjectEvaluationItems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("percentage", models.IntegerField(default=0)),
                (
                    "curriculum",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.curriculumtype",
                    ),
                ),
            ],
        ),
    ]
