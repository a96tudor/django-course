from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, ProfileForm, SkillForm, MessageForm
from .models import UserProfile, Message
from .utils import search_profiles
from utils import get_paginator_for_dataset

# Create your views here.


def profiles(request):
    profiles, query = search_profiles(request)
    profiles, paginator, custom_range = get_paginator_for_dataset(
        profiles, request, 3,
    )

    return render(
        request, 'users/profiles.html',
        {
            'profiles': profiles, 'query': query,
            'custom_range': custom_range,
        },
    )


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
        if 'next' in request.GET:
            return redirect(request.GET['next'])
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
    else:
        messages.error(request, 'Data validation failed!')
        return redirect('edit-account')


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.userprofile

    if request.method == 'GET':
        form = SkillForm()

        return render(
            request, 'users/skill_form.html', {'form': form},
        )

    form = SkillForm(request.POST)

    if form.is_valid():
        skill = form.save(commit=False)
        skill.owner = profile
        skill.save()
        return redirect('user_account')
    else:
        messages.error(request, 'Data validation failed!')
        return redirect('create-skill')


@login_required(login_url='login')
def update_skill(request, pk):
    try:
        profile = request.user.userprofile
        skill = profile.skill_set.get(id=pk)
    except Exception:
        return render(
            request, 'users/no_skill.html', {'id': pk},
        )

    if request.method == 'GET':
        form = SkillForm(instance=skill)

        return render(request, 'users/skill_form.html', {'form': form})

    form = SkillForm(request.POST, instance=skill)

    if form.is_valid():
        form.save()

        return redirect('user_account')
    else:
        messages.error(request, 'Data validation failed!')
        return redirect('update-skill', pk=pk)


@login_required(login_url='login')
def delete_skill(request, pk):
    try:
        profile = request.user.userprofile
        skill = profile.skill_set.get(id=pk)
    except Exception:
        return render(
            request, 'users/no_skill.html', {'id': pk},
        )

    if request.method == 'GET':
        return render(request, 'users/delete_skill.html', {'object': skill})

    skill.delete()
    return redirect('user_account')


@login_required(login_url='login')
def message(request, pk):
    profile = request.user.userprofile
    try:
        message = profile.messages.get(id=pk)
    except Exception:
        messages.error(request, f'No message with id "{pk}"')
        return redirect(request, 'inbox')

    message.read = True
    message.save()

    return render(request, 'users/message.html', {'message': message})


@login_required(login_url='login')
def inbox(request):
    profile = request.user.userprofile
    user_messages = profile.messages.all()
    new_messages_count = user_messages.filter(read=False).count()

    return render(
        request, 'users/inbox.html',
        {'user_messages': user_messages, 'unread_count': new_messages_count}
    )


def send_message(request, pk):
    try:
        recipient = UserProfile.objects.get(id=pk)
    except:
        messages.error(request, f'No user with id "{pk}"')
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            return redirect('profiles')

    if request.method == 'GET':
        form = MessageForm()

        return render(
            request, 'users/new_message.html',
            {'form': form, 'recipient': recipient}
        )

    form = MessageForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)

        try:
            profile = request.user.userprofile
            message.sender = profile
            message.email = profile.email
            message.name = profile.name
        except:
            pass

        message.recipient = recipient
        message.save()

        messages.success(request, f'Message sent to {recipient}!')

        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            return redirect('profiles')

    messages.error(request, 'Failed to send message!')
    return redirect('send-message')
