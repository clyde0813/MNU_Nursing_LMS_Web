# Generated by Django 4.1 on 2024-02-01 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models', '0005_assignmentvideo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklistrecord',
            name='assignment',
        ),
        migrations.AddField(
            model_name='checklistrecord',
            name='curriculum',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.curriculum'),
        ),
        migrations.AddField(
            model_name='checklistrecord',
            name='target',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checklist_target', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='checklistrecord',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
