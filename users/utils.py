from rest_framework_simplejwt.views import TokenObtainPairView

from wallets.models import Wallet


class TokenObtainCustom(TokenObtainPairView):
    """обновить токен + uuid кошелька (для удобства)"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        wallet = Wallet.objects.filter(owner__email=request.data.get("email")).first()
        custom_data = {
            "|": "Убедитесь, что вы поменяли токен в следующих запросах",
        }
        if wallet:
            custom_data["uuid вашего кошелька"] = wallet.uuid

        response.data.update(custom_data)
        return response
