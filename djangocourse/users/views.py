from django.shortcuts import render

from .models import UserProfile

# Create your views here.


def profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'users/profiles.html', {'profiles': profiles})


def user_profile(request, pk):
    user = UserProfile.objects.get(id=pk)
    topskills = user.skill_set.exclude(description__exact='')
    otherskills = user.skill_set.filter(description__exact='')

    return render(
        request, 'users/user-profile.html',
        {'profile': user, 'topskills': topskills, 'otherskills': otherskills},
    )
