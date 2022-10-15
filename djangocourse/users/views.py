from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

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


def login_page(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'GET':
        return render(request, 'users/login_register.html')

    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'Username does not exist!')
        return render(request, 'users/login_register.html')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('profiles')
    else:
        messages.error(request, 'Username or password is incorrect!')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
