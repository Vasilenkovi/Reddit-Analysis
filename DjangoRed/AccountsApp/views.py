from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
from .models import UserAccountManager

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated successfully')
                    return render(request, 'home.html')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': form})

def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = register_form.save()
            return render(request,
                        'accounts/register_done.html',
                        {'new_user': new_user})
    else:
        register_form = UserRegistrationForm()
    return render(request,
                'accounts/register.html',
                {'registration_form': register_form})

@login_required(login_url='/account/login/')
def user_profile(request):
    return render   (request, 
                    'accounts/profile.html')