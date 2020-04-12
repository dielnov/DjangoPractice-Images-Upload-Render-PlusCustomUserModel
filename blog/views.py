from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfileUpdateForm
from .models import Account

# Create your views here.


def index(request):
    context = {}
    if request.method == 'POST':
        try:
            # UpdateProfile If It Exists Already
            profile = request.user.user_profile
            form = ProfileUpdateForm(
                request.POST, request.FILES, instance=profile)
            context['profile'] = profile
            if form.is_valid():
                form.save()
            context['form'] = form
            return redirect('blog:index')
        except:
            # If It Doesnt Exist Then Create One
            form = ProfileUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            context['form'] = form
            return redirect('blog:index')
    else:
        try:
            # Get Profile Into Form If It Exists
            profile = request.user.user_profile
            form = ProfileUpdateForm(instance=profile)
            context['profile'] = profile
        except:
            # Otherwise Get Blank Form
            form = ProfileUpdateForm()
    context['form'] = form
    return render(request, 'blog/index.html', context)


def registration_view(request):
    context = {}
    profile = request.user.profile
    form = ProfileUpdateForm()

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=false)
            instance.user = request.user
            instance.save()

    context['form'] = form
    return render(request, 'blog/index.html', context)
