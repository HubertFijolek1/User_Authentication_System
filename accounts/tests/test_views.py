import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'strongpassword',
        'password2': 'strongpassword',
    })
    assert response.status_code == 302  # Redirect after registration
    assert User.objects.filter(email='test@example.com').exists()

@pytest.mark.django_db
def test_login_lockout(client):
    user = User.objects.create_user('testuser', 'test@example.com', 'correctpassword')
    login_url = reverse('login')
    for _ in range(5):
        response = client.post(login_url, {'username': 'testuser', 'password': 'wrongpassword'})
    # Check that the account is locked
    response = client.post(login_url, {'username': 'testuser', 'password': 'correctpassword'})
    assert 'Account locked' in response.content.decode()