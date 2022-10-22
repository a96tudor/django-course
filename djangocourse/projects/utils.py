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


def get_votes_for_project(project):
    all_reviews = list(project.review_set.all())

    if len(all_reviews) == 0:
        return 0.0, 0

    number_of_positive_votes = len([
        review for review in all_reviews if review.value == 'up'
    ])

    return number_of_positive_votes / len(all_reviews), len(all_reviews)
