# Generated by Django 4.0.5 on 2022-07-01 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_what_you_learn_requirements'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='yt_thumbnail')),
                ('title', models.CharField(max_length=100)),
                ('youtube_id', models.CharField(max_length=200)),
                ('time_duration', models.FloatField(null=True)),
                ('preview', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.lesson')),
            ],
        ),
    ]
