from django.urls import path

from wallets import views
from wallets.apps import WalletsConfig

app_name = WalletsConfig.name

urlpatterns = [
    path(
        "wallets/<uuid:WALLET_UUID>/operation",
        views.WalletOperationView.as_view(),
        name="operation",
    ),
    path("wallets", views.WalletListCreateView.as_view(), name="create"),
    path("wallets/all", views.WalletListView.as_view(), name="list_all"),
    path("wallets/<uuid:WALLET_UUID>", views.WalletListView.as_view(), name="list"),
    path("wallets/<uuid:uuid>/delete", views.WalletDeleteView.as_view(), name="delete"),
]
