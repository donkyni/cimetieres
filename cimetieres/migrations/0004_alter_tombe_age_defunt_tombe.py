# Generated by Django 3.2 on 2021-10-16 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cimetieres', '0003_alter_tombe_deces_defunt_tombe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tombe',
            name='age_defunt_tombe',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
