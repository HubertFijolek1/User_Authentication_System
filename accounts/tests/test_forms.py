import pytest
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserCreationForm:
    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()

    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'WrongPass123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_invalid_form_missing_email(self):
        form_data = {
            'username': 'newuser',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors

class TestCustomAuthenticationForm:
    def test_valid_login(self, django_user_model):
        user = django_user_model.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='loginpassword123',
            is_active=True
        )
        form_data = {
            'username': 'loginuser',
            'password': 'loginpassword123',
        }
        form = CustomAuthenticationForm(data=form_data)
        assert form.is_valid()

    def test_invalid_login(self):
        form_data = {
            'username': 'nonexistent',
            'password': 'wrongpassword',
        }
        form = CustomAuthenticationForm(data=form_data)
        assert not form.is_valid()
        assert '__all__' in form.errors

class TestProfileUpdateForm:
    def test_valid_profile_update(self, django_user_model):
        user = django_user_model.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='profilepassword123',
            is_active=True
        )
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
        }
        form = ProfileUpdateForm(data=form_data, instance=user)
        assert form.is_valid()
        updated_user = form.save()
        assert updated_user.username == 'updateduser'
        assert updated_user.email == 'updated@example.com'

    def test_invalid_profile_update(self, django_user_model):
        user = django_user_model.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='profilepassword123',
            is_active=True
        )
        form_data = {
            'username': '',  # Username is required
            'email': 'invalidemail',  # Invalid email format
        }
        form = ProfileUpdateForm(data=form_data, instance=user)
        assert not form.is_valid()
        assert 'username' in form.errors
        assert 'email' in form.errors
