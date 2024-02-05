# Generated by Django 4.1 on 2024-02-04 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import models.models as modelsmodels


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('content', models.CharField(max_length=1000)),
                ('essential', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.checklist')),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectEvaluationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.IntegerField(default=0)),
                ('post_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.posttype')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.subject')),
            ],
        ),
        migrations.CreateModel(
            name='PostUserMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostSubjectMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.subject')),
            ],
        ),
        migrations.CreateModel(
            name='PostPostMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_post', to='models.post')),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_post', to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=modelsmodels.dynamic_upload_to)),
                ('filename', models.CharField(max_length=100)),
                ('file_extension', models.CharField(max_length=100, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostDeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostChecklistMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.checklistset')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.posttype'),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('confirmed_date', models.DateTimeField(default=None, null=True)),
                ('status', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_author', to=settings.AUTH_USER_MODEL)),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.checklistgroup')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.post')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_target', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='checklistgroup',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.checklistset'),
        ),
    ]
