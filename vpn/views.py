from datetime import timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Sum, Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View, generic
from django.http import HttpResponse
from requests import Response

from .models import Site, Statistic, Customer
from .forms import SiteForm, CustomerCreationForm
from .utils import convert_bytes_to_megabytes


@login_required
def site_create(request) -> HttpResponse:
    error_message = None

    if request.method == "POST":
        form = SiteForm(request.POST)

        if form.is_valid():
            site_name = form.cleaned_data["name"]

            if Site.objects.filter(user=request.user, name=site_name).exists():
                error_message = (
                    f"The site with the name '{site_name}' already exists!"
                )
            else:
                site = form.save(commit=False)
                site.user = request.user
                site.save()
                return redirect("vpn:site-list")
    else:
        form = SiteForm()

    return render(
        request,
        "vpn/site_create.html",
        {"form": form, "error_message": error_message}
    )


class SiteListView(LoginRequiredMixin, generic.ListView):
    model = Site
    paginate_by = 5

    def get_queryset(self) -> QuerySet:
        queryset = Site.objects.filter(user=self.request.user)

        return queryset


class SiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Site


class SiteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Site
    fields = ("name", "url")
    success_url = reverse_lazy("vpn:site-list")


class SiteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Site
    success_url = reverse_lazy("vpn:site-list")


class VPNProxyView(LoginRequiredMixin, View):
    def get(
        self,
        request,
        user_site_name,
        routes_on_original_site,
    ) -> HttpResponse:
        site = Site.objects.get(user=request.user, name=user_site_name)

        if routes_on_original_site == "home":
            routes_on_original_site = ""

        request_url = urljoin(site.url, routes_on_original_site)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(request_url, headers=headers)

        request_size = len(request_url.encode("utf-8"))
        response_size = len(response.content) if response.content else 0

        Statistic.objects.create(
            user=request.user,
            site=site,
            sent_data=request_size,
            received_data=response_size,
        )

        modified_content = self.replace_urls(response, site)

        return HttpResponse(modified_content)

    @staticmethod
    def replace_urls(response: Response, site: Site) -> str:
        soup = BeautifulSoup(response.content, "html.parser")

        for a_tag in soup.select("a"):
            if a_tag.has_attr("href"):
                if a_tag["href"] in [site.url, site.url[:-1]]:
                    a_tag["href"] = f"/vpn/{site.name}/home/"
                elif a_tag["href"].startswith(site.url):
                    routes_on_original_site = (
                        a_tag["href"].replace(site.url, "")
                    )
                    new_href = f"/vpn/{site.name}/{routes_on_original_site}"
                    a_tag["href"] = new_href

        return str(soup)


class CustomerCreateView(generic.CreateView):
    model = Customer
    form_class = CustomerCreationForm


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    fields = ("bio",)


class StatisticListView(LoginRequiredMixin, generic.ListView):
    model = Statistic

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        sites = Site.objects.filter(user=self.request.user)

        context["detailed_statistic"] = self.get_statistic(sites, 28)

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Statistic.objects.filter(user=self.request.user)

        return queryset

    @staticmethod
    def get_statistic(
        sites: QuerySet[Site],
        days: int = 28,
    ) -> dict[str, dict]:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        statistic = {}

        for site in sites:
            results = Statistic.objects.filter(
                site=site,
                timestamp__range=(start_date, end_date),
            ).aggregate(
                uploaded=Sum("sent_data"),
                downloaded=Sum("received_data"),
                transitions_number=Count("id"),
            )

            if results["downloaded"] is not None:
                results["total"] = results["uploaded"] + results["downloaded"]

            statistic[site.name] = {
                key: convert_bytes_to_megabytes(value)
                if value and key != "transitions_number"
                else value
                for key, value in results.items()
            }

        return statistic
