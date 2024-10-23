from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in


User = get_user_model()

def register(request):
    if request.method == 'POST':
        # Process form data
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()
        # Send confirmation email
        mail_subject = 'Activate your account.'
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'from@example.com', [user.email])
        return redirect('account_activation_sent')
    else:
        # Display registration form
        pass

def activate(request, uidb64, token):
    # Activate the user after validating the token
    pass

def login(request):
    if request.method == 'POST':
        # Process login form
        # Check for failed attempts
        pass
    else:
        # Display login form
        pass

def password_reset_request(request):
    if request.method == "POST":
        # Generate token and send password reset email
        pass
    else:
        # Display password reset form
        pass

def password_reset_confirm(request, uidb64, token):
    # Validate token and allow password reset
    pass

@login_required
def profile_update(request):
    if request.method == 'POST':
        # Update user details
        pass
    else:
        # Display profile form
        pass

def logout(request):
    auth_logout(request)
    return redirect('home')