from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects
from utils import get_paginator_for_dataset


# Create your views here.


def projects(request):
    projects, query = search_projects(request)
    projects, paginator, custom_range = get_paginator_for_dataset(
        projects, request, 3,
    )

    return render(
        request, 'projects/projects.html',
        {
            'projects': projects, 'query': query,
            'custom_range': custom_range,
        },
    )


def project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Exception:
        return render(
            request, 'projects/no_skill.html', {'project': {'pk': pk}},
        )
    profile = request.user.userprofile

    already_voted = profile in [review.owner for review in
        project.review_set.all()]

    if request.method == 'GET' or profile == project.owner:
        upvote_perc, number_of_votes = get_votes_for_project(project)
        tags = project.tags.all()

        return render(
            request, 'projects/project.html',
            {
                'project': project, 'form': ReviewForm(),
                'tags': tags, 'profile': profile, 'votes': number_of_votes,
                'upvote_perc': upvote_perc * 100,
                'already_voted': already_voted,
            },
        )

    if already_voted:
        return redirect('project', project.id)

    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.owner = profile
        review.project = project

        review.save()
        project.get_vote_ratio
        messages.success(request, 'Your review was submitted successfully!')

    return redirect('project', project.id)


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
            request, 'projects/no_skill.html', {'project': {'pk': pk}},
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
            request, 'projects/no_skill.html', {'project': {'pk': pk}},
        )

    if request.method == 'GET':
        return render(
            request, 'projects/delete_skill.html', {'object': project},
        )

    project.delete()
    return redirect('projects')
