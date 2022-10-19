from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, ProfileForm
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
        return render(request, 'users/login_register.html', {'page': 'login'})

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

    return redirect('login')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(
            request, 'users/login_register.html',
            {'page': 'register', 'form': form}
        )

    form = UserRegistrationForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()

        user.save()
        messages.success(request, 'User was created successfully!')

        login(request, user)

        return redirect('edit-account')

    else:
        messages.error(request, 'Data validation failed!')
        return redirect('register')


@login_required(login_url='login')
def user_account(request):
    user = request.user.userprofile

    return render(
        request, 'users/account.html',
        {
            'profile': user,
            'skills': user.skill_set.all(),
            'projects': user.project_set.all(),
        },
    )


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.userprofile
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
        return render(request, 'users/profile_form.html', {'form': form})

    form = ProfileForm(request.POST, request.FILES, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('user_account')
