# Generated by Django 2.2.5 on 2019-12-18 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='newpassword',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='新密码'),
        ),
    ]
