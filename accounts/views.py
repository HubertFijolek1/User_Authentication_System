from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.contrib.auth import views as auth_views

UserModel = get_user_model()

# Account lockout settings
from django.core.cache import cache

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 15  # minutes

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email confirmation
            user.save()
            # Send activation email
            current_site = request.get_host()
            subject = 'Activate your account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def activation_sent(request):
    return render(request, 'accounts/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')

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