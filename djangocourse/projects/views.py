from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm


# Create your views here.


def projects(request):
    all_projects = Project.objects.all()
    return render(
        request, 'projects/projects.html', {'projects': all_projects}
    )


def project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Exception:
        return render(
            request, 'projects/no_project.html', {'project': {'pk': pk}},
        )

    tags = project.tags.all()

    return render(
        request, 'projects/project.html', {'project': project, 'tags': tags},
    )


@login_required(login_url='login')
def create_project(request):
    profile = request.user.userprofile
    if request.method == 'GET':
        form = ProjectForm()
        context = {'form': form}
        return render(request, 'projects/project_form.html', context)

    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = profile

        project.save()

        return redirect('projects')


@login_required(login_url='login')
def update_project(request, pk):
    try:
        profile = request.user.userprofile
        project = profile.project_set.get(id=pk)
    except Exception:
        return render(
            request, 'projects/no_project.html', {'project': {'pk': pk}},
        )

    if request.method == 'GET':
        form = ProjectForm(instance=project)
        context = {'form': form}
        return render(request, 'projects/project_form.html', context)

    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects')


@login_required(login_url='login')
def delete_project(request, pk):
    try:
        profile = request.user.userprofile
        project = profile.project_set.get(id=pk)
    except Exception:
        return render(
            request, 'projects/no_project.html', {'project': {'pk': pk}},
        )

    if request.method == 'GET':
        return render(
            request, 'projects/delete_object.html', {'object': project},
        )

    project.delete()
    return redirect('projects')
