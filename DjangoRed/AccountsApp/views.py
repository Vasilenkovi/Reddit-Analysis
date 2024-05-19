from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserChangeDataForm
from .models import UserAccountManager, FavoriteJobIDs
from .db_queries import check_for_up_to_date_job_ids

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
    context = {
        "up_to_date_job_ids": [],
        "expired_job_ids": [],
        "change_data_form": None
    }

    data_form = UserChangeDataForm(initial={
            "date": request.user.date_of_birth,
            "email": request.user.email
        })
    
    if (request.method == "POST"):
        data_form = UserChangeDataForm(data=request.POST)
        if (data_form.is_valid()):
            data = data_form.cleaned_data
            user = get_object_or_404(
                UserAccount,
                username=request.user
            )
            user.date_of_birth = data['date_of_birth']
            user.email = data['email']
            user.save()
    
    up_to_date_job_ids = []
    expired_job_ids = []

    favorite_job_ids = FavoriteJobIDs.objects.filter(username=request.user)
    
    current_job_ids = check_for_up_to_date_job_ids()
    
    for job_id in favorite_job_ids:
        if (job_id.job_id not in current_job_ids):
            expired_job_ids.append(job_id.job_id)
        else:
            up_to_date_job_ids.append(job_id.job_id)

    context["up_to_date_job_ids"] = up_to_date_job_ids
    context["expired_job_ids"] = expired_job_ids
    context["change_data_form"] = data_form

    return render (
        request, 
        'accounts/profile.html',
        context
    )