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

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        cache_key = f'login_attempts_{username}'
        attempts = cache.get(cache_key, 0)
        if attempts >= MAX_FAILED_ATTEMPTS:
            messages.error(request, 'Your account is locked due to multiple failed login attempts. Please try again later.')
            return render(request, 'accounts/login.html', {'form': form})
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            cache.delete(cache_key)  # Reset attempts
            return redirect('home')
        else:
            attempts += 1
            cache.set(cache_key, attempts, LOCKOUT_TIME * 60)
            if attempts >= MAX_FAILED_ATTEMPTS:
                messages.error(request, 'Your account is locked due to multiple failed login attempts. Please try again later.')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def password_reset_request(request):
    if request.method == "POST":
        form = auth_views.PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = UserModel.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    current_site = request.get_host()
                    subject = 'Password Reset Requested'
                    message = render_to_string('accounts/password_reset_email.html', {
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    try:
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                return redirect('password_reset_done')
    else:
        form = auth_views.PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_done_view(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

def password_reset_complete_view(request):
    return render(request, 'accounts/password_reset_complete.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_update')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

