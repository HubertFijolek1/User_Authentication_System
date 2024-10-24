import pytest
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
import re

User = get_user_model()

@pytest.mark.django_db
class TestRegistrationView:
    def test_registration(self, client):
        response = client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        })
        assert response.status_code == 302  # Redirect after registration
        user = User.objects.get(email='testuser@example.com')
        assert not user.is_active
        # Check that an email was sent
        assert len(mail.outbox) == 1

    def test_activation(self, client):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPass123',
            is_active=False
        )
        # Generate activation token
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        response = client.get(activation_url)
        assert response.status_code == 302  # Redirect after activation
        user.refresh_from_db()
        assert user.is_active

@pytest.mark.django_db
class TestLoginView:
    def test_login_with_username(self, client):
        user = User.objects.create_user(
            username='loginuser',
            email='loginuser@example.com',
            password='TestPass123',
            is_active=True
        )
        response = client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'TestPass123',
        })
        assert response.status_code == 302  # Redirect after login
        assert '_auth_user_id' in client.session

    def test_login_with_email(self, client):
        user = User.objects.create_user(
            username='loginuser',
            email='loginuser@example.com',
            password='TestPass123',
            is_active=True
        )
        response = client.post(reverse('login'), {
            'username': 'loginuser@example.com',
            'password': 'TestPass123',
        })
        assert response.status_code == 302
        assert '_auth_user_id' in client.session

    def test_account_lockout(self, client):
        user = User.objects.create_user(
            username='lockoutuser',
            email='lockout@example.com',
            password='TestPass123',
            is_active=True
        )
        login_url = reverse('login')
        cache_key = f'login_attempts_{user.username}'

        for _ in range(settings.MAX_FAILED_ATTEMPTS):
            response = client.post(login_url, {
                'username': 'lockoutuser',
                'password': 'WrongPass123',
            })
            assert response.status_code == 200

        response = client.post(login_url, {
            'username': 'lockoutuser',
            'password': 'TestPass123',
        })
        assert response.status_code == 200
        assert 'Your account is locked' in response.content.decode()

        # Ensure the user cannot log in during lockout period
        assert '_auth_user_id' not in client.session

@pytest.mark.django_db
class TestPasswordResetView:
    def test_password_reset(self, client):
        user = User.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='OldPass123',
            is_active=True
        )
        response = client.post(reverse('password_reset'), {
            'email': 'reset@example.com',
        })
        assert response.status_code == 302  # Redirect after requesting password reset
        assert len(mail.outbox) == 1
        # Extract reset link from email
        email_body = mail.outbox[0].body
        match = re.search(r'http://[^/]+(/reset/\S+)', email_body)
        assert match is not None
        reset_link = match.group(1)
        # Reset password
        response = client.post(reset_link, {
            'new_password1': 'NewPass123',
            'new_password2': 'NewPass123',
        })
        assert response.status_code == 302  # Redirect after password reset
        # Verify new password works
        client.logout()
        response = client.post(reverse('login'), {
            'username': 'resetuser',
            'password': 'NewPass123',
        })
        assert response.status_code == 302
        assert '_auth_user_id' in client.session

@pytest.mark.django_db
class TestProfileUpdateView:
    def test_profile_update(self, client):
        user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='ProfilePass123',
            is_active=True
        )
        client.login(username='profileuser', password='ProfilePass123')
        response = client.post(reverse('profile_update'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        assert response.status_code == 302  # Redirect after profile update
        user.refresh_from_db()
        assert user.username == 'updateduser'
        assert user.email == 'updated@example.com'

@pytest.mark.django_db
class TestTwoFactorAuthenticationView:
    def test_two_factor_setup_access(self, client):
        user = User.objects.create_user(
            username='2fauser',
            email='2fa@example.com',
            password='2faPass123',
            is_active=True
        )
        client.login(username='2fauser', password='2faPass123')
        response = client.get(reverse('two_factor:setup'))
        assert response.status_code == 200
        assert 'Two-Factor Authentication Setup' in response.content.decode()

    # Additional tests for 2FA setup and verification would require a more complex setup
    # involving OTP generation and verification, which is beyond the scope of this example.

@pytest.mark.django_db
class TestLogoutView:
    def test_logout(self, client):
        user = User.objects.create_user(
            username='logoutuser',
            email='logout@example.com',
            password='LogoutPass123',
            is_active=True
        )
        client.login(username='logoutuser', password='LogoutPass123')
        response = client.get(reverse('logout'))
        assert response.status_code == 302  # Redirect after logout
        assert '_auth_user_id' not in client.session

