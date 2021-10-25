
from django.conf.urls import url

from cimetieres import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^division$', views.division, name='division'),
    url(r'^ajouterdivision$', views.ajouterdivision, name='ajouterdivision'),
    url(r'^(?P<id>\d+)/modifierdivision$', views.modifierdivision, name="modifierdivision"),
    url(r'^(?P<id>\d+)/suprimerdivision$', views.supprimerdivision, name="supprimerdivision"),
    url(r'^dimension', views.dimension, name='dimension'),
    url(r'^ajouterdimension$', views.ajouterdimension, name='ajouterdimension'),
    url(r'^(?P<id>\d+)/modifierdimension', views.modifierdimension, name="modifierdimension"),
    url(r'^(?P<id>\d+)/suprimerdimension', views.supprimerdimension, name="supprimerdimension"),
    url(r'^observation$', views.observation, name='observation'),
    url(r'^ajouterobservation$', views.ajouterobservation, name='ajouterobservation'),
    url(r'^(?P<id>\d+)/modifierobservation', views.modifierobservation, name="modifierobservation"),
    url(r'^(?P<id>\d+)/suprimerobservation', views.supprimerobservation, name="supprimerobservation"),
    url(r'^ligne', views.ligne, name='ligne'),
    url(r'^fichier', csrf_exempt(views.fichier), name='fichier'),
    url(r'^compte', views.compte, name='compte'),
    url(r'^utilisateurs', views.utilisateurs, name='utilisateurs'),
    url(r'^createutilisateur', views.createutilisateur, name='createutilisateur'),
    url(r'^(?P<id>\d+)/updateutilisateur', views.updateutilisateur, name="updateutilisateur"),
    url(r'^(?P<id>\d+)/deleteutilisateur', views.deleteutilisateur, name="deleteutilisateur"),
    url(r'^(?P<id>\d+)/activeutilisateur', views.activeutilisateur, name="activeutilisateur"),
    url(r'^profil', views.profil, name='profil'),
    url(r'^createprofil', views.createprofil, name='createprofil'),
    url(r'^(?P<id>\d+)/updateprofil', views.updateprofil, name="updateprofil"),
    url(r'^(?P<id>\d+)/deleteprofil', views.deleteprofil, name="deleteprofil"),
    url(r'^droit', views.droit, name='droit'),
    url(r'^createdroit', views.createdroit, name='createdroit'),
    url(r'^(?P<id>\d+)/updatedroit', views.updatedroit, name="updatedroit"),
    url(r'^(?P<id>\d+)/deletedroit', views.deletedroit, name="deletedroit"),
    url(r'^(?P<id>\d+)/detail-tombe-selectionner', views.detailtombe, name='detailtombe'),
]
