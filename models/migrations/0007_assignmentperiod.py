# Generated by Django 4.1 on 2023-12-12 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_checklistrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.assignment')),
            ],
        ),
    ]
