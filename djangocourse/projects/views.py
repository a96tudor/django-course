from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


projects_list = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'Fully functional e-commerce website',
    },
    {
        'id': '2',
        'title': 'Portfolio Website',
        'description': 'Project where I built my portfolio',
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'Awesome project still on the way',
    }
]


def projects(request):
    return render(
        request, 'projects/projects.html', {'projects': projects_list}
    )


def project(request, pk):
    project = None

    for p in projects_list:
        if p['id'] == pk:
            project = p

    if project is None:
        return render(
            request, 'projects/no_project.html', {'project': {'pk': pk}},
        )

    return render(
        request, 'projects/project.html', {'project': project},
    )
