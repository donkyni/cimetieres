from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from cimetieres.models import Division, Dimension, Observation, Tombe, User, Profils, Droits


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('nom_division',)
        labels = {
            'nom_division': _('Division')
        }
        widgets = {
            'nom_division': forms.TextInput(attrs={'class': 'form-control'})
        }


class DimensionForm(forms.ModelForm):
    class Meta:
        model = Dimension
        fields = ('nom_dimension',)
        labels = {
            'nom_dimension': _('Dimension')
        }
        widgets = {
            'nom_dimension': forms.TextInput(attrs={'class': 'form-control'})
        }


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ('nom_observation',)
        labels = {
            'nom_observation': _('Observation')
        }
        widgets = {
            'nom_observation': forms.TextInput(attrs={'class': 'form-control'})
        }


class TombeForm(forms.ModelForm):
    naissance_defunt_tombe = forms.DateField(widget=DateInput)
    deces_defunt_tombe = forms.DateField(widget=DateInput)
    age_defunt_tombe = forms.IntegerField()

    class Meta:
        model = Tombe
        fields = ('division', 'cadastre_tombe', 'emplacement_tombe', 'nom_defunt_tombe', 'naissance_defunt_tombe',
                  'deces_defunt_tombe', 'age_defunt_tombe', 'dimension', 'observation')
        labels = {
            'cadastre_tombe': _('Cadastre'),
            'emplacement_tombe': _('Emplacement'),
            'nom_defunt_tombe': _('Nom du defunt'),
            'naissance_defunt_tombe': _('Date de naissance du defunt'),
            'deces_defunt_tombe': _('Date de décès du defunt'),
            'age_defunt_tombe': _('Age du defunt'),
        }
        widgets = {
            'division': forms.TextInput(attrs={'class': 'form-control'}),
            'dimension': forms.TextInput(attrs={'class': 'form-control'}),
            'observation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse', 'telephone', 'profil', 'avatar', 'sexe')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'pseudo', 'nom', 'prenom', 'adresse', 'telephone', 'profil', 'avatar', 'sexe')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'nom', 'prenom', 'adresse', 'telephone', 'sexe', 'avatar'
        )


class ProfilsForm(forms.ModelForm):
    class Meta:
        model = Profils
        fields = ('nom',)
        labels = {
            'nom': _('Nom du profil')
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }


class DroitsForm(forms.ModelForm):
    class Meta:
        model = Droits
        fields = ('nom',)
        labels = {
            'nom': _('Nom du droit')
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }
