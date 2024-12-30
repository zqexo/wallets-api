from django.db import transaction
from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["uuid", "balance", "owner"]


class WalletOperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=["DEPOSIT", "WITHDRAW"])
    amount = serializers.DecimalField(max_digits=25, decimal_places=2)

    @staticmethod
    def validate_amount(value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной.")
        return value

    def update_wallet_balance(self, wallet):
        """Обновление баланса кошелька в зависимости от типа операции."""
        operation_type = self.validated_data["operationType"]
        amount = self.validated_data["amount"]

        # Блокировка транзакции на уровне базы данных для обеспечения атомарности
        with transaction.atomic():
            wallet.refresh_from_db()  # Обновление состояния кошелька из базы данных

            if operation_type == "DEPOSIT":
                wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if wallet.balance < amount:
                    raise serializers.ValidationError("Недостаточно средств на счете.")
                wallet.balance -= amount

            wallet.save()
        return wallet
