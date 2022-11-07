# Generated by Django 4.1.1 on 2022-11-07 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='alert_send_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время напоминания'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, to='web.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=500, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.tag'),
        ),
        migrations.CreateModel(
            name='NoteComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='Текст')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='web.note', verbose_name='Заметка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
