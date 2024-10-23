# User Authentication System

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Migration](#database-migration)
  - [Running the Server](#running-the-server)
- [Testing](#testing)
- [Continuous Integration and Deployment (CI/CD)](#continuous-integration-and-deployment-cicd)
- [Usage](#usage)
  - [User Registration](#user-registration)
  - [Email Confirmation](#email-confirmation)
  - [Login](#login)
  - [Account Lockout](#account-lockout)
  - [Password Reset](#password-reset)
  - [Profile Update](#profile-update)
  - [Two-Factor Authentication](#two-factor-authentication)
  - [Logout](#logout)
- [Detailed Functionality Analysis](#detailed-functionality-analysis)
  - [1. User Registration with Email Confirmation](#1-user-registration-with-email-confirmation)
  - [2. Password Hashing](#2-password-hashing)
  - [3. Email Verification](#3-email-verification)
  - [4. Login with Email or Username](#4-login-with-email-or-username)
  - [5. Account Lockout After Failed Login Attempts](#5-account-lockout-after-failed-login-attempts)
  - [6. Password Reset via Email](#6-password-reset-via-email)
  - [7. Password Reset Token Validation](#7-password-reset-token-validation)
  - [8. User Profile Update](#8-user-profile-update)
  - [9. Two-Factor Authentication (2FA)](#9-two-factor-authentication-2fa)
  - [10. Logout Functionality](#10-logout-functionality)
- [Additional Features to Consider](#additional-features-to-consider)
- [Security Considerations](#security-considerations)
- [Contact Information](#contact-information)

---

## Features

1. **Register a New User with Username, Email, and Password**
2. **Hash Passwords Before Saving to the Database**
3. **Send Confirmation Email with Verification Link**
4. **Login Using Email or Username with Password Validation**
5. **Lock User Account After Multiple Failed Login Attempts**
6. **Reset Password via Email with Secure Token Link**
7. **Validate Password Reset Token and Allow New Password Submission**
8. **Update User Details in Profile Section**
9. **Enable Two-Factor Authentication for Enhanced Security**
10. **Logout Functionality with Session Invalidation**

---

## Technologies Used

- **Python 3.8+**
- **Django 3.2+**
- **Django Two-Factor Authentication**
- **SQLite3 (default) or PostgreSQL**
- **pytest and pytest-django for Testing**
- **GitHub Actions for CI/CD**

---

## Project Structure

```
auth_system/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_forms.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── auth_backend.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── User_Authentication/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── base_generic.html
├── manage.py
├── requirements.txt
├── pytest.ini
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Virtual Environment tool (optional but recommended)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/auth_system.git
   cd auth_system
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following (replace with your actual values):

   ```env
   SECRET_KEY='your-secret-key'
   EMAIL_HOST='smtp.your-email-provider.com'
   EMAIL_PORT=587
   EMAIL_HOST_USER='your-email@example.com'
   EMAIL_HOST_PASSWORD='your-email-password'
   EMAIL_USE_TLS=True
   ```

   **Note:** For development purposes, the email backend is set to console in `settings.py`. Update the email backend and settings when configuring for production.

5. **Update Database Settings (Optional)**

   If you prefer to use PostgreSQL or another database, update the `DATABASES` setting in `User_Authentication/settings.py`.

### Database Migration

Apply database migrations:

```bash
python manage.py migrate
```

### Running the Server

Start the development server:

```bash
python manage.py runserver
```

---

## Testing

Run tests using pytest:

```bash
pytest
```

Ensure that `pytest` and `pytest-django` are installed (already included in `requirements.txt`).

---

## Continuous Integration and Deployment (CI/CD)

The project is set up with GitHub Actions for CI/CD.

- **CI/CD Configuration File:** `.github/workflows/ci.yml`
- **Actions:**
  - Runs tests on every push and pull request to the `main` branch.
  - Can be extended to include deployment steps.

---

## Usage

### User Registration

- Navigate to `http://localhost:8000/accounts/register/`.
- Fill out the registration form with a username, email, and password.
- Upon successful submission, a confirmation email is sent.

### Email Confirmation

- Check the console output for the activation link (since the email backend is set to console).
- Click the activation link to activate your account.

### Login

- Navigate to `http://localhost:8000/accounts/login/`.
- Login using your email or username and password.

### Account Lockout

- After 5 failed login attempts, the account is locked for 15 minutes.
- A message will inform you about the lockout duration.

### Password Reset

- Navigate to `http://localhost:8000/accounts/password_reset/`.
- Enter your registered email address.
- Check the console output for the password reset link.
- Click the link to reset your password.

### Profile Update

- Navigate to `http://localhost:8000/accounts/profile/` (login required).
- Update your email and username.

### Two-Factor Authentication

- Navigate to `http://localhost:8000/account/two_factor/` (login required).
- Follow the instructions to set up 2FA using an authenticator app.

### Logout

- Click the logout link in the navigation menu.
- Session is invalidated upon logout.

---

## Detailed Functionality Analysis

### 1. User Registration with Email Confirmation

**Files Involved:**

- `accounts/models.py`
- `accounts/forms.py`
- `accounts/views.py`
- `accounts/templates/accounts/register.html`

**Implementation Details:**

- **Custom User Model (`accounts/models.py`):**
  - Inherits from `AbstractBaseUser` and `PermissionsMixin`.
  - Uses email as the primary identifier (`USERNAME_FIELD = 'email'`).
  - Custom `UserManager` handles user creation with `create_user` and `create_superuser`.

- **Registration Form (`accounts/forms.py`):**
  - `CustomUserCreationForm` extends `UserCreationForm` to include `email` and `username`.

- **Registration View (`accounts/views.py`):**
  - Handles GET and POST requests for user registration.
  - On POST, validates the form and saves the user with `is_active=False`.
  - Sends an activation email (see Functionality 3).

- **Registration Template (`accounts/templates/accounts/register.html`):**
  - Renders the registration form using Django's templating language.

**Alternatives:**

- Using Django's default `User` model.
- Extending the user model with a profile model.
- Using third-party libraries like `django-allauth`.

**Pros and Cons:**

- **Pros:**
  - Flexibility and control over the user model.
  - Allows for future extensions and customizations.

- **Cons:**
  - Increased complexity and maintenance.
  - Potential compatibility issues with third-party apps.

### 2. Password Hashing

**Implementation Details:**

- **Automatic Hashing:**
  - Handled by Django's `AbstractBaseUser`.
  - `user.set_password(password)` hashes the password using Django's password hashers.

**Alternatives:**

- Custom password hashing mechanisms (not recommended).
- Delegating authentication to third-party systems.

**Pros and Cons:**

- **Pros:**
  - Secure and reliable hashing.
  - Follows best security practices.

- **Cons:**
  - Less control over hashing algorithms.

### 3. Email Verification

**Files Involved:**

- `accounts/views.py`
- `accounts/templates/accounts/activation_email.html`
- `accounts/urls.py`

**Implementation Details:**

- **Activation Email:**
  - Uses `send_mail` to send an email with an activation link.
  - `default_token_generator` generates a secure token.
  - The activation link includes `uidb64` and `token`.

- **Activation View:**
  - Validates the token and activates the user.
  - Logs the user in upon successful activation.

**Alternatives:**

- Using `django-registration`.
- Asynchronous email sending with Celery.
- Third-party email services like SendGrid.

**Pros and Cons:**

- **Pros:**
  - Simple and secure implementation.
  - Full control over email content.

- **Cons:**
  - Synchronous email sending may affect performance.
  - Requires additional configuration for email deliverability.

### 4. Login with Email or Username

**Files Involved:**

- `accounts/auth_backend.py`
- `accounts/forms.py`
- `accounts/views.py`
- `settings.py`

**Implementation Details:**

- **Custom Authentication Backend (`accounts/auth_backend.py`):**
  - Allows authentication with either email or username.
  - Overrides the `authenticate` method.

- **Custom Authentication Form (`accounts/forms.py`):**
  - Modifies the login form to accept email or username.

- **Settings Configuration:**
  - Registers the custom backend in `AUTHENTICATION_BACKENDS`.

**Alternatives:**

- Using only email or username for authentication.
- Using `django-allauth` for multiple authentication methods.

**Pros and Cons:**

- **Pros:**
  - Provides flexibility and convenience for users.

- **Cons:**
  - Additional complexity in authentication logic.

### 5. Account Lockout After Failed Login Attempts

**Files Involved:**

- `accounts/views.py`

**Implementation Details:**

- **Failed Login Tracking:**
  - Uses Django's cache framework to track failed attempts.
  - Locks the account after exceeding `MAX_FAILED_ATTEMPTS`.

- **Lockout Duration:**
  - Accounts are locked for `LOCKOUT_TIME` minutes.

**Alternatives:**

- Storing failed attempts in the database.
- Using third-party packages like `django-axes`.

**Pros and Cons:**

- **Pros:**
  - Simple implementation without additional dependencies.

- **Cons:**
  - Cache may not persist across server restarts.
  - Not suitable for multi-server environments without a shared cache.

### 6. Password Reset via Email

**Files Involved:**

- `accounts/views.py`
- `accounts/templates/accounts/password_reset_email.html`
- `accounts/urls.py`

**Implementation Details:**

- **Password Reset Form:**
  - Uses Django's `PasswordResetForm`.
  - Sends an email with a password reset link.

- **Email Template:**
  - Custom email template for the password reset email.

**Alternatives:**

- Using `django-rest-framework` and JWT tokens.
- Third-party packages for password reset workflows.

**Pros and Cons:**

- **Pros:**
  - Secure and reliable using Django's built-in mechanisms.

- **Cons:**
  - Limited customization of internal processes.

### 7. Password Reset Token Validation

**Files Involved:**

- `accounts/views.py`
- `accounts/templates/accounts/password_reset_confirm.html`
- `accounts/urls.py`

**Implementation Details:**

- **Token Validation:**
  - Uses Django's `PasswordResetConfirmView`.
  - Validates the token and allows the user to set a new password.

- **Template:**
  - Custom template for the password reset confirmation page.

**Alternatives:**

- Custom implementation of token validation (not recommended).

**Pros and Cons:**

- **Pros:**
  - Secure and well-tested.

- **Cons:**
  - Limited customization.

### 8. User Profile Update

**Files Involved:**

- `accounts/forms.py`
- `accounts/views.py`
- `accounts/templates/accounts/profile_update.html`

**Implementation Details:**

- **Profile Update Form:**
  - `ProfileUpdateForm` allows users to update their email and username.

- **Profile Update View:**
  - Handles updating the user's profile.
  - Protected by `login_required` decorator.

**Alternatives:**

- Using class-based views like `UpdateView`.
- Separate forms for different profile fields.

**Pros and Cons:**

- **Pros:**
  - Simple and straightforward.

- **Cons:**
  - May need to extend for additional profile fields.

### 9. Two-Factor Authentication (2FA)

**Files Involved:**

- `User_Authentication/settings.py`
- `User_Authentication/urls.py`

**Implementation Details:**

- **Dependencies:**
  - Uses `django-two-factor-auth` and `django-otp`.

- **Configuration:**
  - Adds necessary apps and middleware.
  - Includes 2FA URLs.

**Alternatives:**

- Custom 2FA implementation (complex and risky).
- Using other 2FA packages.

**Pros and Cons:**

- **Pros:**
  - Enhances security significantly.

- **Cons:**
  - Adds complexity to the authentication process.
  - May impact user experience.

### 10. Logout Functionality

**Files Involved:**

- `accounts/views.py`
- `accounts/urls.py`

**Implementation Details:**

- **Logout View:**
  - Uses Django's `logout` function to invalidate the session.

**Alternatives:**

- Using class-based views like `LogoutView`.
- Token invalidation for token-based authentication systems.

**Pros and Cons:**

- **Pros:**
  - Simple and effective.

- **Cons:**
  - Limited to session-based authentication.

---

## Additional Features to Consider

- **Email Backend Configuration:**
  - Use a real SMTP server for sending emails in production.
  - Secure email credentials using environment variables.

- **User Roles and Permissions:**
  - Implement different user roles (admin, moderator, user).
  - Use Django's permission system to restrict access.

- **Social Authentication:**
  - Integrate social login options using `django-allauth`.

- **Account Deactivation and Reactivation:**
  - Allow users to deactivate/reactivate their accounts.

- **Email Change Confirmation:**
  - Send a confirmation email when a user changes their email address.

- **Improved UI/UX:**
  - Enhance the front-end using Bootstrap or another CSS framework.
  - Ensure the application is responsive and accessible.

- **Logging and Monitoring:**
  - Implement logging to track user activities.
  - Use monitoring tools to track application performance.

- **Security Enhancements:**
  - Implement HTTPS with SSL/TLS certificates.
  - Set security headers to protect against common vulnerabilities.

---

## Security Considerations

- **Password Hashing:** Passwords are securely hashed using Django's built-in password management system.
- **Email Confirmation:** Accounts must be activated via email to prevent spam registrations.
- **Account Lockout:** Prevents brute-force attacks by locking accounts after multiple failed login attempts.
- **Two-Factor Authentication:** Adds an extra layer of security for user accounts.
- **Session Security:** Sessions are invalidated upon logout to prevent unauthorized access.

---

## Contact Information

For any questions or suggestions, please open an issue or contact the project maintainer at [hubertfijolek1@gmail.com](mailto:hubertfijolek1@gmail.com).

---

**Note:** This project is intended for educational purposes and may require additional configuration for production use. Always ensure sensitive information is secured using environment variables or a secrets management system.
