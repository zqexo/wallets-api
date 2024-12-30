from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from wallets.models import Wallet
from wallets.serializers import WalletOperationSerializer, WalletSerializer


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletListView(generics.ListAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        wallet_uuid = self.kwargs.get("WALLET_UUID")
        if wallet_uuid:
            queryset = Wallet.objects.filter(uuid=wallet_uuid)
            if not queryset.exists():
                raise NotFound(detail="Кошелек не найден")
            return queryset
        return Wallet.objects.all()


class WalletOperationView(generics.GenericAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletOperationSerializer

    def get_object(self):
        try:
            return Wallet.objects.get(uuid=self.kwargs["WALLET_UUID"])
        except Wallet.DoesNotExist:
            raise NotFound(detail="Кошелек не найден")

    def post(self, request, *args, **kwargs):
        wallet = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                wallet = serializer.update_wallet_balance(wallet)
                return Response(WalletSerializer(wallet).data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDeleteView(generics.DestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            try:
                wallet = self.get_object()
                wallet.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Wallet.DoesNotExist:
                raise NotFound(detail="Кошелек не найден")
