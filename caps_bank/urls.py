from django.contrib import admin
from django.urls import include, path
from account.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("account.urls")),
    path("transfers/", include("transfers.urls")),
    path("investments/", include("investments.urls")),
    path("", HomeView.as_view(), name="home"),
]
