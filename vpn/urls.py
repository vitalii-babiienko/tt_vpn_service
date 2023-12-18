from django.urls import path

from vpn.views import (
    SiteListView,
    site_create,
    SiteDetailView,
    SiteUpdateView,
    SiteDeleteView,
    VPNProxyView,
    CustomerCreateView,
    CustomerDetailView,
    CustomerUpdateView,
    StatisticListView,
)

urlpatterns = [
    path(
        "sites/",
        SiteListView.as_view(),
        name="site-list",
    ),
    path(
        "sites/create/",
        site_create,
        name="site-create",
    ),
    path(
        "sites/<int:pk>/",
        SiteDetailView.as_view(),
        name="site-detail",
    ),
    path(
        "sites/<int:pk>/update/",
        SiteUpdateView.as_view(),
        name="site-update",
    ),
    path(
        "sites/<int:pk>/delete/",
        SiteDeleteView.as_view(),
        name="site-delete",
    ),
    path(
        "customers/create/",
        CustomerCreateView.as_view(),
        name="customer-create",
    ),
    path(
        "customers/<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail",
    ),
    path(
        "customers/<int:pk>/update/",
        CustomerUpdateView.as_view(),
        name="customer-update",
    ),
    path(
        "statistics/",
        StatisticListView.as_view(),
        name="statistic-list",
    ),
    path(
        "<str:user_site_name>/<path:routes_on_original_site>/",
        VPNProxyView.as_view(),
        name="vpn-proxy",
    ),
]

app_name = "vpn"
