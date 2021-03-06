# Generated by Django 3.1 on 2020-12-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('month', models.IntegerField(default=0)),
                ('day', models.IntegerField(default=0)),
                ('hour', models.IntegerField(default=0)),
                ('T1H', models.FloatField()),
                ('SKY', models.FloatField(default=0)),
                ('RN1', models.FloatField()),
                ('REH', models.FloatField()),
                ('PTY', models.FloatField()),
                ('VEC', models.FloatField()),
                ('WSD', models.FloatField()),
                ('S06', models.FloatField()),
            ],
            options={
                'db_table': 'weather',
            },
        ),
    ]
