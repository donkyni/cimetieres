from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from cimetieres.models import Division, Dimension, Observation, Tombe, User, Droits, Profils, DroitsProfils

from import_export.admin import ImportExportModelAdmin


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


class TombeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
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


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse',
            'telephone', 'avatar', 'sexe',
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse',
            'telephone', 'avatar', 'sexe', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class DroitsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'archive')
    list_filter = ('nom',)
    ordering = ('nom',)
    search_fields = ('nom',)


admin.site.register(Droits, DroitsAdmin)


class ProfilsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'archive')
    list_filter = ('nom',)
    ordering = ('nom',)
    search_fields = ('nom',)


admin.site.register(Profils, ProfilsAdmin)


class DroitsProfilsAdmin(admin.ModelAdmin):
    list_display = ('profil', 'droit', 'ecriture', 'lecture', 'modification', 'suppression')
    list_filter = ('profil', 'droit')
    ordering = ('profil',)
    search_fields = ('profil',)


admin.site.register(DroitsProfils, DroitsProfilsAdmin)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'pseudo', 'nom', 'prenom', 'adresse',
        'telephone', 'profil', 'avatar', 'sexe', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'nom')
    fieldsets = (
        (None, {'fields': ('pseudo', 'password')}),
        ('Personal info', {'fields': (
            'nom', 'prenom', 'adresse',
            'telephone', 'profil', 'avatar', 'sexe',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'pseudo', 'nom', 'prenom', 'adresse',
                'telephone', 'profil', 'avatar', 'sexe', 'password'),
        }),
    )
    search_fields = ('pseudo', 'nom',)
    ordering = ('date_d_ajout',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
