from django.db.models import Q

from .models import Skill, UserProfile


def search_profiles(request):
    query = ''

    if request.GET.get('search-query'):
        query = request.GET.get('search-query')

    skills = Skill.objects.filter(name__iexact=query)

    profiles = UserProfile.objects.distinct().filter(
        Q(name__icontains=query) |
        Q(short_intro__icontains=query) |
        Q(skill__in=skills)
    )

    return profiles, query
