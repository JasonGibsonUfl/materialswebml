# Generated by Django 3.1.7 on 2021-02-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlmodel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svrmodel',
            name='pickle_str',
            field=models.TextField(),
        ),
    ]
