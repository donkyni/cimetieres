from django.contrib import admin

from cimetieres.models import Division, Dimension, Observation, Tombe


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('nom_division', 'date_de_creation_division', 'archive_division',)
    list_filter = ('nom_division',)
    date_hierarchy = 'date_de_creation_division'
    ordering = ('nom_division',)
    search_fields = ('nom_division',)


admin.site.register(Division, DivisionAdmin)


class DimensionAdmin(admin.ModelAdmin):
    list_display = ('nom_dimension', 'date_creation_dimension', 'archive_dimension',)
    list_filter = ('nom_dimension',)
    date_hierarchy = 'date_creation_dimension'
    ordering = ('nom_dimension',)
    search_fields = ('nom_dimension',)


admin.site.register(Dimension, DimensionAdmin)


class ObservationAdmin(admin.ModelAdmin):
    list_display = ('nom_observation', 'date_creation_observation', 'archive_observation',)
    list_filter = ('nom_observation',)
    date_hierarchy = 'date_creation_observation'
    ordering = ('nom_observation',)
    search_fields = ('nom_observation',)


admin.site.register(Observation, ObservationAdmin)


class TombeAdmin(admin.ModelAdmin):
    list_display = ('division', 'cadastre_tombe', 'emplacement_tombe', 'nom_defunt_tombe',
                    'naissance_defunt_tombe', 'deces_defunt_tombe', 'age_defunt_tombe',
                    'dimension', 'observation', 'date_enregistrement',)
    list_filter = ('division', 'cadastre_tombe', 'emplacement_tombe', 'nom_defunt_tombe',
                   'naissance_defunt_tombe', 'deces_defunt_tombe', 'age_defunt_tombe',
                   'dimension', 'observation', 'date_enregistrement',)
    date_hierarchy = 'date_enregistrement'
    ordering = ('division', 'cadastre_tombe', 'emplacement_tombe', 'nom_defunt_tombe',
                'naissance_defunt_tombe', 'deces_defunt_tombe', 'age_defunt_tombe',
                'dimension', 'observation', 'date_enregistrement',)
    search_fields = ('division', 'cadastre_tombe', 'emplacement_tombe', 'nom_defunt_tombe',
                     'naissance_defunt_tombe', 'deces_defunt_tombe', 'age_defunt_tombe',
                     'dimension', 'observation', 'date_enregistrement',)


admin.site.register(Tombe, TombeAdmin)
