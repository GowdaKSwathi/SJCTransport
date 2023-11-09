from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from accounts.forms import CreateUserForm, ProfileForm
from accounts.models import Profile
from .decorators import unauthenticated_user
from accounts.decorators import allowed_users

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #create group for user and add user to group
            group = Group.objects.get_or_create(name = 'principal')
            user.groups.add(group[0])
            #create profile
            Profile.objects.create(user=user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'OOPS! Username Or Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

# logout
@login_required
def logoutUser(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('username')
    return response


@login_required
@allowed_users(allowed_roles=['principal','operator'])
def settingsPage(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
    context = {'form': form,"room_name":"broadcast"}
    return render(request, 'accounts/settings.html', context)
