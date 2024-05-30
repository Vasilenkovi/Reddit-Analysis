from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts_app'

urlpatterns = [
    path('profile/', views.user_profile, name='profile'),
    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # change password urls
    path(
        'password-change/',
        views.password_change,
        name='password_change'
    ),
    path(
        'password-change/done/',
        views.password_change_done,
        name='password_change_done'
    ),

    # reset password urls
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    

    # path('', views.dashboard, name='dashboard'),
]
