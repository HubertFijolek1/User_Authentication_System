from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

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
