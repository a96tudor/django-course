from django.db.models import Q

from .models import Project, Tag


def search_projects(request):
    query = ''

    if request.GET.get('query'):
        query = request.GET.get('query')

    tags = Tag.objects.filter(name__iexact=query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__in=tags) |
        Q(owner__name__icontains=query)
    )

    return projects, query
