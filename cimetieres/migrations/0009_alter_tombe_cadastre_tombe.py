# Generated by Django 3.2 on 2021-10-18 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cimetieres', '0008_alter_tombe_nom_defunt_tombe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tombe',
            name='cadastre_tombe',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
