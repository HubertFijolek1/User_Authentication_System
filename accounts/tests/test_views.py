import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'StrongPassword123',
        'password2': 'StrongPassword123',
    })
    assert response.status_code == 302  # Redirect after registration
    assert User.objects.filter(email='test@example.com').exists()
    user = User.objects.get(email='test@example.com')
    assert not user.is_active  # Inactive until email confirmation
    assert len(mail.outbox) == 1
    assert 'Activate your account' in mail.outbox[0].subject

@pytest.mark.django_db
def test_login_lockout(client):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='correctpassword', is_active=True)
    login_url = reverse('login')
    for _ in range(5):
        client.post(login_url, {'username': 'testuser', 'password': 'wrongpassword'})
    response = client.post(login_url, {'username': 'testuser', 'password': 'correctpassword'})
    assert 'Your account is locked' in response.content.decode()
