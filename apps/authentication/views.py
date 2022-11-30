# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from termcolor import colored
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
import random
import string
from apps.home.models import User_Other_Fields, Plan
import smtplib
import ssl
from django.contrib.auth import logout as auth_logout
import requests


sender = 'taha.hamedani8@gmail.com'
password = '61416867'

mailgun_API_key = '9e8c72a90aa54ca4871cda665cfbcd57-054ba6b6-7986a744'
mailgun_domain = 'profilebrowse.com'

############################################# Emails ##########################################################

def send_email_from_admin_to_client(user, message_ticket):

    receiver = user.email
    user_name = user.username

    try_count = 1

    while try_count < 10:
        try:
            try_count += 1
            "curl -s --user 'api:9e8c72a90aa54ca4871cda665cfbcd57-054ba6b6-7986a744' https://api.mailgun.net/v3/profilebrowse.com/messages -F from='Taha Hamedani <taha_hamedani@profilebrowse.com>' -F to=taha.hamedani8@gmail.com -F subject='Hello' -F text='Testing some Mailgun awesomeness!'"
            
            # mailgun configuration
            return requests.post(
            "https://api.mailgun.net/v3/" + mailgun_domain + "/messages",
            auth=("api", mailgun_API_key),
            data={"from": "profilebrowse Support <support@" + mailgun_domain +">",
                "to": [receiver],
                "subject": "Ticket From Admin",
                "template": "ticket_admin",
                "h:X-Mailgun-Variables": "{\"body\": \"" + message_ticket + "\"}"})


        except Exception as e:
            print(colored(e,'red'))
            print (colored("Error: unable to send email",'red'))
            # return False

    print (colored("Error: unable to send email",'red'))
    return False

def send_email_from_client_to_admin(user, message_ticket):
    
    receiver = 'taha_hamedani@yahoo.com'
    user_name = user.username
    user_email = user.email
    sender = 'taha.hamedani8@gmail.com'

    try_count = 1

    while try_count < 10:
        try:
            try_count += 1
            "curl -s --user 'api:9e8c72a90aa54ca4871cda665cfbcd57-054ba6b6-7986a744' https://api.mailgun.net/v3/profilebrowse.com/messages -F from='Taha Hamedani <taha_hamedani@profilebrowse.com>' -F to=taha.hamedani8@gmail.com -F subject='Hello' -F text='Testing some Mailgun awesomeness!'"
            
            # mailgun configuration
            return requests.post(
            "https://api.mailgun.net/v3/" + mailgun_domain + "/messages",
            auth=("api", mailgun_API_key),
            data={"from": "profilebrowse Support <support@" + mailgun_domain +">",
                "to": ["taha_hamedani@yahoo.com"],
                "subject": "New Ticket",
                "template": "ticket_client",
                "h:X-Mailgun-Variables": "{\"client_name\": \"" + user_email + "\", \"body\": \"" + message_ticket + "\"}"})


        except Exception as e:
            print(colored(e,'red'))
            print (colored("Error: unable to send email",'red'))
            # return False

    print (colored("Error: unable to send email",'red'))
    return False

def send_activation_user_email(user, usre_key):

    # receiver = 'taha_hamedani@yahoo.com'
    receiver = user.email
    user_name = user.username

    try_count = 1

    while try_count < 10:
        try:
            try_count += 1
            "curl -s --user 'api:9e8c72a90aa54ca4871cda665cfbcd57-054ba6b6-7986a744' https://api.mailgun.net/v3/profilebrowse.com/messages -F from='Taha Hamedani <taha_hamedani@profilebrowse.com>' -F to=taha.hamedani8@gmail.com -F subject='Hello' -F text='Testing some Mailgun awesomeness!'"
            
            activation_url = 'https://profilebrowse.com/activate_user_' + str(usre_key)
            # activation_url = 'http://127.0.0.1:8000/activate_user_' + str(usre_key)

            # mailgun configuration
            return requests.post(
            "https://api.mailgun.net/v3/" + mailgun_domain + "/messages",
            auth=("api", mailgun_API_key),
            data={"from": "profilebrowse Support <support@" + mailgun_domain +">",
                "to": [receiver],
                "subject": "Email Verification",
                "template": "email_verify",
                "h:X-Mailgun-Variables": "{\"client_name\": \"" + user_name + "\", \"activation_url\": \"" + activation_url + "\"}"})


        except Exception as e:
            print(colored(e,'red'))
            print (colored("Error: unable to send email",'red'))
            # return False

    print (colored("Error: unable to send email",'red'))
    return False

def send_new_user_notification_email(user_email):

    receiver = 'taha_hamedani@yahoo.com'
    

    try_count = 1

    while try_count < 10:
        try:
            try_count += 1
            "curl -s --user 'api:9e8c72a90aa54ca4871cda665cfbcd57-054ba6b6-7986a744' https://api.mailgun.net/v3/profilebrowse.com/messages -F from='Taha Hamedani <taha_hamedani@profilebrowse.com>' -F to=taha.hamedani8@gmail.com -F subject='Hello' -F text='Testing some Mailgun awesomeness!'"
            
            # mailgun configuration
            return requests.post(
            "https://api.mailgun.net/v3/" + mailgun_domain + "/messages",
            auth=("api", mailgun_API_key),
            data={"from": "profilebrowse Support <support@" + mailgun_domain +">",
                "to": [receiver],
                "subject": "New User Registered",
                "template": "newuser",
                "h:X-Mailgun-Variables": "{\"client_email\": \"" + user_email + "\"}"})


        except Exception as e:
            print(colored(e,'red'))
            print (colored("Error: unable to send email",'red'))
            # return False

    print (colored("Error: unable to send email",'red'))
    return False
        
############################################# User Models ##########################################################

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("/dashboard_admin/")
                else:
                    return redirect("/dashboard_client/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "home/page-sign-in.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
    
        form = SignUpForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get("email")

            user_email_find_list = User.objects.filter(email=email)
            if(user_email_find_list and len(user_email_find_list) > 0):
                msg = 'Form is not valid'
                return render(request, "home/page-sign-up.html", {"form": form, "msg": msg, "success": success, "form_email_errors": 'A user with that email already exists.'})


            form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=email, password=raw_password)
            
            user_created = sorted(User.objects.all().filter(email=email), key = lambda x: x.date_joined, reverse = True)[0]
            user_created.is_active = False
            user_created.save()

            # add user_key to user_other_fields table
            user_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            free_plan = Plan.objects.all().filter(price= 0)[0]

            user_other_fields_obj = User_Other_Fields(user = user_created, user_key = user_key, plan = free_plan)
            user_other_fields_obj.save()

            # send activation email to user
            send_status = send_activation_user_email(user_created,user_key)
            # send_test_email()
            if (send_status):
                msg = 'Activation Email has send to your email. please click on activation link'
                success = True

            else:
                # delete unsuccessfull send email user in order to try again
                delete_user_records(user_created, user_other_fields_obj)
                msg = 'Unable to send Activation Email to your email'

            # return redirect("/login/")
            return render(request, "home/page-sign-up.html", {"form": form, "msg": msg, "success": success})


        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "home/page-sign-up.html", {"form": form, "msg": msg, "success": success})

def change_password_client(request):
    msg = None
    success = False
    
    if request.method == "POST": # just in confirm new bulk data buttton clicked

        try:
            # current_password = request.POST.get('current_password').strip()
            email = request.POST.get('email').strip()
        

            new_password_1 = request.POST.get('new_password_1').strip()
            new_password_2 = request.POST.get('new_password_2').strip()

            if (new_password_1 != new_password_2):
                msg = 'new passwords are not the same !'
                return render(request, "home/profile_client.html", {"msg": msg, "success": success})

            try:
                password_validation.validate_password(new_password_1)
            except Exception as e:
                msg = str(e)
                return render(request, "home/profile_client.html", {"msg": msg, "success": success})

            request.user.set_password(new_password_1)
            request.user.save()

            msg = 'user password changed successfully ! '
            success = True

        except Exception as e:
            print(e)
            msg= str(e)
            success = False

    return render(request, "home/profile_client.html", {"msg": msg, "success": success})

def change_password_admin(request):
    msg = None
    success = False
    
    if request.method == "POST": # just in confirm new bulk data buttton clicked

        try:
            # current_password = request.POST.get('current_password').strip()
            email = request.POST.get('email').strip()
        

            new_password_1 = request.POST.get('new_password_1').strip()
            new_password_2 = request.POST.get('new_password_2').strip()

            if (new_password_1 != new_password_2):
                msg = 'new passwords are not the same !'
                return render(request, "home/profile_client.html", {"msg": msg, "success": success})

            try:
                password_validation.validate_password(new_password_1)
            except Exception as e:
                msg = str(e)
                return render(request, "home/profile_client.html", {"msg": msg, "success": success})

            request.user.set_password(new_password_1)
            request.user.save()

            msg = 'user password changed successfully ! '
            success = True

        except Exception as e:
            print(e)
            msg= str(e)
            success = False

    return render(request, "home/profile_admin.html", {"msg": msg, "success": success})

def activate_user(request):
    msg = 'your user is activated. You can sing in !!!'

    user_key = request.path.split('activate_user_')[-1]

    user_id = User_Other_Fields.objects.filter(user_key=user_key)[0].user_id

    user_created = User.objects.filter(id=user_id)[0]


    user_created.is_active = True
    user_created.save()

    # try to login with activated user
    if user_created is not None:

        user_created.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user_created)

        # send new user sign up notification to admin
        send_new_user_notification_email(user_created.email)

        if user_created.is_superuser:
            return redirect("/dashboard_admin/")
        else:
            return redirect("/dashboard_client/")
    else:
        msg = 'Invalid credentials'


    success = True
    form = None
    
    return render(request, "home/page-sign-in.html", {"form": form, "msg": msg})

def delete_user_records(user_created, user_other_fields_created):
    try:
        user_other_fields_created.delete()
        user_created.delete()
        print(colored('user records deleted !', 'green'))
    except Exception as e:
        print(colored(e))

def login_with_google(request):
    
    try:
        user_other_fields_find = User_Other_Fields.objects.filter(user_id=request.user.id)
        if (len(user_other_fields_find) == 0):
            # add user_key to user_other_fields table
            user_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            free_plan = Plan.objects.all().filter(price= 0)[0]
            user_other_fields_obj = User_Other_Fields(user = request.user, user_key = user_key, plan = free_plan)
            user_other_fields_obj.save()

            # send new user sign up notification to admin
            send_new_user_notification_email(request.user.email)

    except Exception as e:
        print(e)

    return redirect("/dashboard_client/")

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect ('/login/')

def resend_email_user_admin(request):
    user_id = 0
    try:

        user_id = 0
        user_id_string = '0'
        try:
            user_id_string = request.path.split('/user_')[-1]
        except Exception as e:
            pass

        user_id = int(user_id_string)
        user_selected = User.objects.get(id= user_id)

         # select user_key
        user_key = User_Other_Fields.objects.get(user_id= user_id).user_key
        print(colored(user_key, 'blue'))

        # send activation email to user
        send_status = send_activation_user_email(user_selected, user_key)
    
    except Exception as e:
        print(colored('Exception in sendin verification email ' + str(e), 'red'))

    return redirect ('/userslist_admin/')

