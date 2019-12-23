# Generated by Django 2.2.5 on 2019-12-19 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0004_auto_20191219_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='手机'),
        ),
        migrations.AddField(
            model_name='student',
            name='sex',
            field=models.IntegerField(choices=[(0, '男'), (1, '女'), (2, '未知')], default=2, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='student',
            name='studentname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='姓名'),
        ),
        migrations.AlterUniqueTogether(
            name='problem_knowledge',
            unique_together={('course_problem', 'course_knowledge')},
        ),
        migrations.AlterUniqueTogether(
            name='student_course_problem',
            unique_together={('student', 'course_problem')},
        ),
    ]
