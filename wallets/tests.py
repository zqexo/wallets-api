import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from wallets.models import Wallet


class WalletAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create(
            email="admin@test.test",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.admin_user.set_password("admin123")
        self.admin_user.save()

        # Создание обычного пользователя
        self.regular_user = User.objects.create(
            email="user@test.test",
            is_active=True,
        )
        self.regular_user.set_password("user123")
        self.regular_user.save()

    def create_wallet(self, user, balance=100):
        return Wallet.objects.create(owner=user, balance=balance)

    # WalletListCreateView Tests
    def test_wallet_list(self):
        self.create_wallet(self.admin_user, balance=200)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("http://127.0.0.1:8000/api/v1/wallets/all")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_wallet_create(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            "http://127.0.0.1:8000/api/v1/wallets",
            {"balance": 500, "owner": self.admin_user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)

    def test_wallet_list_by_uuid(self):
        wallet = self.create_wallet(self.admin_user, balance=300)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_list_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            "http://127.0.0.1:8000/api/v1/wallets/nonexistent-uuid/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_operation_deposit(self):
        wallet = self.create_wallet(self.admin_user, balance=100)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}/operation",
            {"operationType": "DEPOSIT", "amount": 50},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, 150)

    def test_wallet_operation_withdraw(self):
        wallet = self.create_wallet(self.admin_user, balance=100)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}/operation",
            {"operationType": "WITHDRAW", "amount": 50},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, 50)

    def test_wallet_operation_insufficient_funds(self):
        wallet = self.create_wallet(self.admin_user, balance=100)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}/operation",
            {"operationType": "WITHDRAW", "amount": 150},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Недостаточно средств", response.data["error"])

    def test_wallet_delete_by_admin(self):
        wallet = self.create_wallet(self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}/delete"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

    def test_wallet_delete_by_regular_user(self):
        wallet = self.create_wallet(self.regular_user)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/wallets/{wallet.uuid}/delete"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wallet_delete_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(
            "http://127.0.0.1:8000/api/v1/wallets/nonexistent-uuid/delete"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
