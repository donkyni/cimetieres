from django.db import models


class Division(models.Model):
    nom_division = models.CharField(max_length=255, null=True)
    date_de_creation_division = models.DateField(auto_now_add=True, null=True)
    archive_division = models.BooleanField(default=False, null=True)


class Dimension(models.Model):
    nom_dimension = models.CharField(max_length=255, null=True)
    date_creation_dimension = models.DateField(auto_now_add=True)
    archive_dimension = models.BooleanField(default=False, null=True)


class Observation(models.Model):
    nom_observation = models.CharField(max_length=255, null=True)
    date_creation_observation = models.DateField(auto_now_add=True, null=True)
    archive_observation = models.BooleanField(default=False, null=True)


class Tombe(models.Model):
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    cadastre_tombe = models.IntegerField(null=True)
    emplacement_tombe = models.CharField(max_length=255, null=True)
    nom_defunt_tombe = models.CharField(max_length=255, null=True)
    naissance_defunt_tombe = models.DateField(null=True)
    deces_defunt_tombe = models.DateField(null=True)
    age_defunt_tombe = models.IntegerField(null=True)
    dimension = models.ForeignKey(Dimension, on_delete=models.SET_NULL, null=True)
    observation = models.ForeignKey(Observation, on_delete=models.SET_NULL, null=True)
    date_enregistrement = models.DateField(auto_now_add=True, null=True)
    archive_tombe = models.BooleanField(default=False, null=True)
