# Generated by Django 3.2 on 2021-10-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cimetieres', '0005_alter_tombe_age_defunt_tombe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tombe',
            name='age_defunt_tombe',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
