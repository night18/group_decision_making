# Generated by Django 3.2.13 on 2023-03-04 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practicerecord',
            old_name='human_estimation',
            new_name='final_answer',
        ),
        migrations.AddField(
            model_name='practicerecord',
            name='initial_answer',
            field=models.CharField(default=False, max_length=10),
            preserve_default=False,
        ),
    ]
