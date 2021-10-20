import json
from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from cimetieres.forms import DivisionForm, DimensionForm, ObservationForm, TombeForm, UserUpdateForm, UserCreationForm, \
    UserForm
from cimetieres.models import Division, Dimension, Observation, Tombe, User


def save_all(request, form, template_name, model, template_name2, mycontext):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if model == "division":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "dimension":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "observation":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
            if model == "utilisateur":
                systeme = form.save(commit=False)
                systeme.save()
                data['form_is_valid'] = True
                data[model] = render_to_string(template_name2, mycontext)
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dashboard(request):
    count_deces = Tombe.objects.filter(archive_tombe=False).count()
    caveau_enfant = Tombe.objects.filter(dimension="Caveau Enfant", archive_tombe=False).count()
    normal = Tombe.objects.filter(dimension="o", archive_tombe=False).count() + Tombe.objects.filter(
        dimension="O", archive_tombe=False).count()
    addition = Tombe.objects.filter(dimension="Addition", archive_tombe=False).count()
    none = Tombe.objects.filter(dimension=None, archive_tombe=False).count()

    context = {
        'count_deces': count_deces,
        'caveau_enfant': caveau_enfant,
        'normal': normal,
        'addition': addition,
        'none': none
    }
    return render(request, 'dashboard/dashboard.html', context)


def division(request):
    divisions = Division.objects.filter(archive_division=False)

    context = {'divisions': divisions}
    return render(request, 'division/division.html', context)


def ajouterdivision(request):
    divisions = Division.objects.filter(archive_division=False)

    context = {'divisions': divisions}

    if request.method == 'POST':
        form = DivisionForm(request.POST)
    else:
        form = DivisionForm()

    return save_all(request, form, 'division/ajouterdivision.html', 'division', 'division/listedivision.html', context)


def modifierdivision(request, id):
    divisions = Division.objects.filter(archive_division=False)
    mycontext = {
        'divisions': divisions
    }
    division = get_object_or_404(Division, id=id)
    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
    else:
        form = DivisionForm(instance=division)
    return save_all(request, form, 'division/modifierdivision.html', 'division', 'division/listedivision.html',
                    mycontext)


def supprimerdivision(request, id):
    data = dict()
    division = get_object_or_404(Division, id=id)
    if request.method == "POST":
        division.archive_division = True
        division.save()
        data['form_is_valid'] = True
        divisions = Division.objects.filter(archive_division=False)
        data['division'] = render_to_string('division/listedivision.html', {'divisions': divisions})
    else:
        context = {
            'division': division,
        }
        data['html_form'] = render_to_string('division/supprimerdivision.html', context, request=request)

    return JsonResponse(data)


def dimension(request):
    dimensions = Dimension.objects.filter(archive_dimension=False)

    context = {'dimensions': dimensions}
    return render(request, 'dimension/dimension.html', context)


def ajouterdimension(request):
    dimensions = Dimension.objects.filter(archive_dimension=False)

    context = {'dimensions': dimensions}

    if request.method == 'POST':
        form = DimensionForm(request.POST)
    else:
        form = DimensionForm()

    return save_all(request, form, 'dimension/ajouterdimension.html', 'dimension',
                    'dimension/listedimension.html', context)


def modifierdimension(request, id):
    dimensions = Dimension.objects.filter(archive_dimension=False)
    mycontext = {
        'dimensions': dimensions
    }
    dimension = get_object_or_404(Dimension, id=id)
    if request.method == 'POST':
        form = DimensionForm(request.POST, instance=dimension)
    else:
        form = DimensionForm(instance=dimension)
    return save_all(request, form, 'dimension/modifierdimension.html', 'dimension',
                    'dimension/listedimension.html', mycontext)


def supprimerdimension(request, id):
    data = dict()
    dimension = get_object_or_404(Dimension, id=id)
    if request.method == "POST":
        dimension.archive_dimension = True
        dimension.save()
        data['form_is_valid'] = True
        dimensions = Dimension.objects.filter(archive_dimension=False)
        data['dimension'] = render_to_string('dimension/listedimension.html', {'dimensions': dimensions})
    else:
        context = {
            'dimension': dimension,
        }
        data['html_form'] = render_to_string('dimension/supprimerdimension.html', context, request=request)

    return JsonResponse(data)


def observation(request):
    observations = Observation.objects.filter(archive_observation=False)

    context = {
        'observations': observations
    }
    return render(request, 'observation/observation.html', context)


def ajouterobservation(request):
    observations = Observation.objects.filter(archive_observation=False)

    context = {'observations': observations}

    if request.method == 'POST':
        form = ObservationForm(request.POST)
    else:
        form = ObservationForm()

    return save_all(request, form, 'observation/ajouterobservation.html', 'observation',
                    'observation/listeobservation.html', context)


def modifierobservation(request, id):
    observations = Observation.objects.filter(archive_observation=False)
    mycontext = {
        'observations': observations
    }
    observation = get_object_or_404(Observation, id=id)
    if request.method == 'POST':
        form = ObservationForm(request.POST, instance=observation)
    else:
        form = ObservationForm(instance=observation)
    return save_all(request, form, 'observation/modifierobservation.html', 'observation',
                    'observation/listeobservation.html', mycontext)


def supprimerobservation(request, id):
    data = dict()
    observation = get_object_or_404(Observation, id=id)
    if request.method == "POST":
        observation.archive_observation = True
        observation.save()
        data['form_is_valid'] = True
        observations = Observation.objects.filter(archive_observation=False)
        data['observation'] = render_to_string('observation/listeobservation.html', {'observations': observations})
    else:
        context = {
            'observation': observation,
        }
        data['html_form'] = render_to_string('observation/supprimerobservation.html', context, request=request)

    return JsonResponse(data)


def ligne(request):
    if request.method == 'POST':
        form = TombeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ligne')
    else:
        form = TombeForm()
    current_date = datetime.now()
    context = {
        'form': form
    }
    return render(request, 'tombe/ligne.html', locals())


def fichier(request):
    tombes = Tombe.objects.filter(archive_tombe=False)

    context = {
        'tombes': tombes
    }
    return render(request, 'tombe/fichier.html', locals())


def compte(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Vos informations ont été bien modifiés !')
            redirect('compte')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'compte/moncompte.html', context)


def utilisateurs(request):
    utilisateurs = User.objects.all()
    context = {
        'utilisateurs': utilisateurs
    }
    return render(request, 'compte/utilisateurs.html', context)


def createutilisateur(request):
    utilisateurs = User.objects.all()
    mycontext = {
        'utilisateurs': utilisateurs
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
    else:
        form = UserCreationForm()
    return save_all(request, form, 'compte/createutilisateur.html',
                    'utilisateur', 'compte/listutilisateur.html', mycontext)


def updateutilisateur(request, id):
    utilisateurs = User.objects.all()
    mycontext = {
        'utilisateurs': utilisateurs
    }
    utilisateur = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=utilisateur)
    else:
        form = UserForm(instance=utilisateur)
    return save_all(request, form, 'compte/updateutilisateur.html',
                    'utilisateur', 'compte/listutilisateur.html', mycontext)


def deleteutilisateur(request, id):
    data = dict()
    utilisateur = get_object_or_404(User, id=id)
    if request.method == "POST":
        utilisateur.is_active = False
        utilisateur.save()
        data['form_is_valid'] = True
        utilisateurs = User.objects.all()
        data['utilisateur'] = render_to_string('compte/listutilisateur.html',
                                               {'utilisateurs': utilisateurs})
    else:
        context = {
            'utilisateur': utilisateur
        }
        data['html_form'] = render_to_string('compte/deleteutilisateur.html', context, request=request)

    return JsonResponse(data)


def activeutilisateur(request, id):
    data = dict()
    utilisateur = get_object_or_404(User, id=id)
    if request.method == "POST":
        utilisateur.is_active = True
        utilisateur.save()
        data['form_is_valid'] = True
        utilisateurs = User.objects.all()
        data['utilisateur'] = render_to_string('compte/listutilisateur.html',
                                               {'utilisateurs': utilisateurs})
    else:
        context = {
            'utilisateur': utilisateur
        }
        data['html_form'] = render_to_string('compte/activeutilisateur.html', context, request=request)

    return JsonResponse(data)
