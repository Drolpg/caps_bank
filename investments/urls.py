from django.urls import path
from .views import (InvestmentCreateView,
                    MyInvestmentsListView,
                    MyInvestmentsRescueView,
                    ProductDetailView,
                    ProductListView)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path(
        "products/<int:product_id>/",
        ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "Investment/<int:product_id>/",
        InvestmentCreateView.as_view(),
        name="investment_create",
    ),
    path("my-investments/",
         MyInvestmentsListView.as_view(), name="my_investments"),
    path(
        "my-investments/<int:investment_id>/",
        MyInvestmentsListView.as_view(),
        name="myinvestment_detail",
    ),
    path(
        "my-investments-rerscue/<int:investment_id>/",
        MyInvestmentsRescueView.as_view(),
        name="myinvestment_rescue",
    ),
]
