import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='strongpassword123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('strongpassword123')
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_active  # Assuming user is inactive until email confirmation

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123'
        )
        assert user.username == 'adminuser'
        assert user.email == 'admin@example.com'
        assert user.check_password('adminpassword123')
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active  # Superuser is active by default

    def test_user_string_representation(self):
        user = User.objects.create_user(
            username='stringtest',
            email='stringtest@example.com',
            password='password'
        )
        assert str(user) == 'stringtest@example.com'
