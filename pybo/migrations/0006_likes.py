# Generated by Django 4.0.3 on 2024-03-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0005_qna_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('writedate', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
    ]
