from django.shortcuts import render
from .models import Project

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
