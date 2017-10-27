from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import IntegrityError
from .models import *
from ..constants import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import *
from django.views.decorators.csrf import csrf_exempt
import smtplib

@csrf_exempt
def editProfile(request):

    # Grab the query parameters; note that .GET must be used to grab parameters from the actual URL
    username = request.GET.get(username_param)
    newPassword = request.GET.get(newPassword_param)
    forgot = request.GET.get(forgot_param)

    if forgot == "1":
        # is username valid?
        # 1. check if it's a usc email
        #   1.1 Contains the usc.edu domain
        #   1.2 email actually works (PING the email)
        # 2. check if username already exists in database

        # 1.1 Contains usc.edu domain
        uscDomain = "@usc.edu"
        uscDomainLength = len(uscDomain)
        username = username.lower()
        if username[-uscDomainLength:] == uscDomain:
            user = None
            try:
                user = UserProfile.objects.get(username=username)

                # 1.2 send email
                sendEmail(username, knowItAllEmail, knowItAllEmailPassword, 'Know It All Email confirmation',
                          changePassMessage(username, newPassword))

                return JsonResponse({'status': 200,
                                     'message': "Successfully sent email confirmation to update password.",
                                     'data': {'username': user.username, 'newPassword': newPassword}}
                                    , status=200)

            # User does not exist
            except ObjectDoesNotExist:
                return JsonResponse(USER_400, status=400)

            # User doesn't exist
            except IntegrityError:
                return JsonResponse(USER_400, status=400)

        else:
            # does not contain @usc.edu as the domain
            return JsonResponse(register_400_INV, status=400, safe=False)

    try:
        u = UserProfile.objects.get(username=username)
        u.password = newPassword
        u.save()
        return JsonResponse({'status': 200,
                         'message': "Successfully saved new password for user " + username,
                         'data': {'newPassword': newPassword }}
                        , status=200)

    except IntegrityError:
        return JsonResponse(UNIQUE_400, status=400)

    # User does not exist
    except ObjectDoesNotExist:
        return JsonResponse(USER_400, status=400)

#sends email
#TODO figure put how to put a subject
def sendEmail(to, from_, from_password, subject, content):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(from_, from_password)
    print(content)
    mail.sendmail(from_, to, content)
    mail.close()

class ChangePassword(FormView):
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, 'password_reset_confirm.html', {
    #     'form': form
    # })