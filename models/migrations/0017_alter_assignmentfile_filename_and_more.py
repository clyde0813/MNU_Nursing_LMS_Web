# Generated by Django 4.2.9 on 2024-01-17 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0016_assignmentfile_filename_curriculumfile_filename"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignmentfile",
            name="filename",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="curriculumfile",
            name="filename",
            field=models.CharField(max_length=100),
        ),
    ]
