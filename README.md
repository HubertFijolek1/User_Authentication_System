# User Authentication System

A Django-based web application implementing a comprehensive user authentication system with the following functionalities:

1. **User Registration with Email Confirmation**
2. **Password Hashing**
3. **Email Verification**
4. **Login with Email or Username**
5. **Account Lockout After Failed Login Attempts**
6. **Password Reset via Email**
7. **Password Reset Token Validation**
8. **User Profile Update**
9. **Two-Factor Authentication (2FA)**
10. **Logout Functionality**

---

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
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

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
- **Django REST Framework**
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
├── auth_system/
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

   If you prefer to use PostgreSQL or another database, update the `DATABASES` setting in `auth_system/settings.py`.

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

- Navigate to `http://localhost:8000/accounts/register/`
- Fill out the registration form with username, email, and password.
- Upon successful submission, a confirmation email is sent.

### Email Confirmation

- Check the console output for the activation link (since the email backend is set to console).
- Click the activation link to activate your account.

### Login

- Navigate to `http://localhost:8000/accounts/login/`
- Login using your email or username and password.

### Account Lockout

- After 5 failed login attempts, the account is locked for 15 minutes.
- A message will inform you about the lockout duration.

### Password Reset

- Navigate to `http://localhost:8000/accounts/password_reset/`
- Enter your registered email address.
- Check the console output for the password reset link.
- Click the link to reset your password.

### Profile Update

- Navigate to `http://localhost:8000/accounts/profile/` (login required)
- Update your email and username.

### Two-Factor Authentication

- Navigate to `http://localhost:8000/account/two_factor/` (login required)
- Follow the instructions to set up 2FA using an authenticator app.

### Logout

- Click the logout link in the navigation menu.
- Session is invalidated upon logout.

---

## Security Considerations

- **Password Hashing:** Passwords are securely hashed using Django's built-in password management system.
- **Email Confirmation:** Accounts must be activated via email to prevent spam registrations.
- **Account Lockout:** Prevents brute-force attacks by locking accounts after multiple failed login attempts.
- **Two-Factor Authentication:** Adds an extra layer of security for user accounts.
- **Session Security:** Sessions are invalidated upon logout to prevent unauthorized access.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write your code and add tests.
4. Ensure all tests pass and the code complies with the project's coding standards.
5. Submit a pull request with a detailed description of your changes.

---

**Note:** This project is intended for educational purposes and may require additional configuration for production use. Always ensure sensitive information is secured using environment variables or a secrets management system.

---

**Contact Information**

For any questions or suggestions, please open an issue or contact the project maintainer at [hubertfijolek1@gmail.com](mailto:hubertfijolek1@gmail.com).