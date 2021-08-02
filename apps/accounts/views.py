from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, render_to_response
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect

from apps.accounts.forms import ContactForm, SetPassword
from apps.accounts.helpers import email_validation_check, check_if_password_match
from apps.accounts.models import User, Contact
from rest_framework.decorators import api_view
from django.db import IntegrityError


@api_view(('GET', 'POST'))
def get_signup_page(request):
    """
    :param request:
    :return:
    """
    context = {}
    return render(request, 'sign_up.html', context)


@api_view(('GET', 'POST'))
def signup_user(request):
    """
    :param request:
    :return:
    """
    context = dict()
    try:
        context["status"] = False
        context["message"] = "Something went wrong"
        signup_data = request.POST
        if email_validation_check(signup_data.get("email")):
            context["first_name"] = signup_data.get("first_name")
            context["last_name"] = signup_data.get("last_name")
            context["email"] = signup_data.get("email")
            context["pass"] = signup_data.get("pass")
            context["re_pass"] = signup_data.get("re_pass")

            if check_if_password_match(context["pass"], context["re_pass"]):
                new_user = User.objects.create_user(username=context["email"], email=context["email"],
                                                    first_name=context["first_name"],
                                                    last_name=context["last_name"],
                                                    password=context["pass"])
                if new_user:
                    context["status"] = True
                    context["message"] = "Successfully registered!"
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    return Response(context, status=status.HTTP_200_OK)
            else:
                context["status"] = False
                context["message"] = "Your password does not match!"
        else:
            context["status"] = False
            context["message"] = "Enter valid email address!"

    except IntegrityError:
        return Response({"status": False, "message": "Email address already exists!"})

    except Exception as e:
        return Response(context, status=status.HTTP_200_OK)

    return Response(context, status=status.HTTP_200_OK)


def login_user(request):
    context = dict()
    context["message"] = ""
    if request.method == 'POST':
        email = request.POST.get('your_email')
        password = request.POST.get('your_pass')
        try:
            user = User.objects.get(email__iexact=email)
            if check_password(password, user.password):
                user = authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    context["message"] = "Login success"
                    return HttpResponseRedirect('/warlord-soft/dashboard/')
                else:
                    context["message"] = "Authentication problem occurred"
            else:
                context["message"] = "Incorrect password!"

        except User.DoesNotExist:
            context["message"] = "User does not exist!"

    if request.user.is_authenticated:
        return redirect("/warlord_soft/dashboard")

    return render(request, 'login.html', context)


# Create your views here.
def home(request):
    context = {}
    return render(request, 'landing_page.html', context)


@api_view(('GET', 'POST'))
def login_request(request):
    context = dict()
    context["message"] = ""
    context["status"] = False
    if request.POST:
        email = request.POST.get('your_email')
        password = request.POST.get('your_pass')
        try:
            user = User.objects.get(email__iexact=email)
            if check_password(password, user.password):
                user = authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    context["message"] = ""
                    context["status"] = True
                    context["redirect_url"] = '/warlord_soft/dashboard/'
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context["message"] = "Authentication problem occurred"
            else:
                context["message"] = "Incorrect password!"

        except User.DoesNotExist:
            context["message"] = "User does not exist!"
    return Response(context, status=status.HTTP_200_OK)


def logout_user(request):
    logout(request)
    return redirect('login')


def change_password(request):
    context = {}
    return render(request, 'password_reset/password_reset_complete.html', context)


def handler404(request, exception, template_name="error_handler/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    return render(request, 'error_handler/500.html', status=500)


def contact_create(request):
    user = request.user
    is_signed_in = False
    if not user.is_anonymous:
        is_signed_in = True
        user = user
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = Contact()
            obj.email = form.cleaned_data['email']
            obj.subject = form.cleaned_data['subject']
            obj.message = form.cleaned_data['message']
            obj.save()
            return redirect('thanks')
    return render(request, "contact_us.html", {'form': form, 'is_signed_in': is_signed_in, 'user': user})


@login_required(login_url='/login/')
def set_your_password(request):
    user = request.user
    is_signed_in = True
    user = user
    if not user.has_usable_password():
        if request.method == 'GET':
            form = SetPassword()
        else:
            form = SetPassword(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get("password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if check_if_password_match(password, confirm_password):
                    user = User.objects.get(email=user.email)
                    user.set_password(password)
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('set_password_success')
                else:
                    return redirect('set_password_fail')

        return render(request, "set_password.html", {'form': form, 'is_signed_in': is_signed_in,
                                                     'user': user, 'hide_form': False,
                                                     'failed': False,
                                                     'authorised': True
                                                     })
    else:
        return render(request, "set_password.html", {'is_signed_in': is_signed_in,
                                                     'user': user, 'hide_form': True,
                                                     'failed': True,
                                                     'authorised': False
                                                     })


@login_required(login_url='/login/')
def set_your_password_success(request):
    user = request.user
    is_signed_in = True
    user = user
    return render(request, "set_password.html", {'is_signed_in': is_signed_in,
                                                 'user': user, 'hide_form': True,
                                                 'failed': False,
                                                 'authorised': True
                                                 })


@login_required(login_url='/login/')
def set_your_password_failed(request):
    user = request.user
    is_signed_in = True
    user = user
    return render(request, "set_password.html", {'is_signed_in': is_signed_in,
                                                 'user': user, 'hide_form': True,
                                                 'failed': True,
                                                 'authorised': True
                                                 })
