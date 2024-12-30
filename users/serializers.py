from rest_framework import serializers

from users.models import User
from wallets.models import Wallet


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Создаем кошелек для пользователя
        wallet = Wallet.objects.create(owner=user)
        return user
