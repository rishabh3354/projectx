from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_reset/change_password.html',
            success_url='/change_password'
        ),
        name='change-password'
    ),


    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/password_reset_form.html',
             subject_template_name='password_reset/password_reset_subject.txt',
             html_email_template_name='password_reset/password_reset_email.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
