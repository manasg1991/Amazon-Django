from email.message import EmailMessage

from django.contrib import messages
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.conf import settings


# Create your views here.
def register(request):
    if request.method == 'POST':

        email = request.POST.get('email', '').strip()

        # Check duplicate email
        if Account.objects.filter(email__iexact=email).exists():
            messages.error(request, "Account with this Email already exists.")
            return redirect('register')

        form = RegistrationForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split('@')[0]

            # Check duplicate username
            if Account.objects.filter(username=username).exists():

                messages.error(
                    request,
                    "This username is already taken. Please choose a different username."
                )

            else:
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password
                )

                user.phone_number = phone_number
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                
                to_email = email
                send_email = EmailMessage(mail_subject,message,settings.DEFAULT_FROM_EMAIL,[email])

                send_email.content_subtype = 'html'

                try:
                    result = send_email.send(fail_silently=False)

                    if result == 1:
                        messages.success(request,"Verification email sent successfully. Please check your inbox.")
                        return redirect('/accounts/login/?command=verification&email=' + email)

                except Exception as e:
                    print("EMAIL ERROR:", repr(e))
                    messages.error(request,"Unable to send verification email. Please try again.")
                    return redirect('register')

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    return render(request,'accounts/login.html')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to the login page after logout

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')   

def forgotpassword(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip()

        user = Account.objects.filter(email__iexact=email).first()

        if user:

            current_site = get_current_site(request)

            mail_subject = 'Reset Your Password'

            message = render_to_string(
                'accounts/reset_password_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )

            to_email = email

            send_email = EmailMessage(
                mail_subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [to_email]
            )

            send_email.content_subtype = 'html'

            try:
                result = send_email.send(fail_silently=False)

                print("PASSWORD RESET EMAIL RESULT:", result)

                if result == 1:
                    messages.success(
                        request,
                        "Password reset email has been sent to your email address."
                    )
                else:
                    messages.error(request, "Unable to send password reset email.")

            except Exception as e:
                print("PASSWORD RESET EMAIL ERROR:", repr(e))
                messages.error(request, "Unable to send password reset email.")

            return redirect('login')

        else:
            messages.error(request, "Account with this email does not exist.")
            return redirect('forgotpassword')

    return render(request, 'accounts/forgotpassword.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('login') 



def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')             


                

            
