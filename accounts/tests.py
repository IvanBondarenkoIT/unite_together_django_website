from django.test import TestCase

from accounts.models import Account


# Create your tests here.

class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            username='john',
            email='johndoe@example.com',
            password='very_secret_password',
        )

    def test_user_creation(self):
        self.assertEqual(Account.objects.count(), 1)

    def test_user_fields(self):
        user = Account.objects.get(pk=1)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'johndoe@example.com')

    def test_user_str(self):
        user = Account.objects.get(pk=1)
        self.assertEqual(str(user), 'John Doe')