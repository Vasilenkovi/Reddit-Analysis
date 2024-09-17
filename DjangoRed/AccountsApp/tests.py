from django.test import TestCase
from django.shortcuts import redirect
from AccountsApp.forms import UserRegistrationForm
from django.test import Client
from django.contrib import auth
from AccountsApp.models import UserAccount
# Create your tests here.
class authorization_test(TestCase):
    def setUp(self):
        UserAccount.objects.create_user("Tester!Login2543)", "adfasdfbh@mail.ru", "1923-02-12", "Y&*IFG^f567fiu8&8g")
        self.clients = Client()
    def test_accessibility(self):
        response = redirect("login/")
        self.assertEqual(response.status_code, 302)
    def test_login(self):
        response = self.clients.login(username="Tester!Login2543)", password="Y&*IFG^f567fiu8&8g")
        self.assertTrue(response)
        user = auth.get_user(self.clients)
        self.assertTrue(user.is_authenticated)

class registration_test(TestCase):
    def setUp(self):
        self.clients = Client()
    def test_accessibility(self):
        response = redirect("view.register")
        self.assertEqual(response.status_code, 302)
    def test_restrictions(self):
        data = {
            'username': 'testuser1SF!',
            'email': 'testuser@example.com',
            'password1': 'testpasswordf3q2!@132',
            'password2': 'testpasswordf3q2!@132',
            "date_of_birth" : "1923-02-12asdfg"
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        data = {
            'username': 'testuser1SF!',
            'email': 'testuser@example.com',
            'password1': 'testpasswordf3q2!@132',
            'password2': 'testpasswordf3q2!@sdfg132',
            "date_of_birth" : "1923-02-12"
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        data = {
            'username': 'testuser1SF!',
            'email': 'testuser@example.com',
            'password1': 'testpasswordf',
            'password2': 'testpasswordf',
            "date_of_birth" : "1923-02.12"
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpasswordf3q2!@132',
            'password2': 'testpasswordf3q2!@132',
            "date_of_birth" : "1923-02-12asdfg"
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        data = {
            'username': 'testuser1SF!',
            'email': 'testusermple.com',
            'password1': 'testpasswordf3q2!@132',
            'password2': 'testpasswordf3q2!@132',
            "date_of_birth" : "1923-02-12asdfg"
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
    def test_creation(self):
        data = {
            'username': 'testuser1SF!',
            'email': 'testuser@example.com',
            'password1': 'testpasswordf3q2!@132',
            'password2': 'testpasswordf3q2!@132',
            "date_of_birth": "1923-02-12"
        }
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())
        response = self.clients.post("/account/register/", {"registration_form": form})
        self.assertEqual(response.status_code, 200)

