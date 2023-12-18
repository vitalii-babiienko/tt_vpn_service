from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vpn.models import Site, Customer

SITE_LIST_URL = reverse("vpn:site-list")
NUMBER_OF_SITES = 8


def create_sites(customer: Customer) -> list[Site]:
    return [
        Site.objects.create(
            user=customer,
            name=f"test_name_{i}",
            url=f"https://test-{i}.ua/",
        )
        for i in range(NUMBER_OF_SITES)
    ]


class PublicSiteListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(SITE_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vpn/sites/",
        )


class PrivateSiteListTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="test_customer",
            password="1qazcde3",
        )
        self.client.force_login(self.customer)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get("/vpn/sites/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(SITE_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(SITE_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "vpn/site_list.html",
        )

    def test_correct_pagination_on_first_page(self) -> None:
        create_sites(self.customer)
        response = self.client.get(SITE_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["site_list"]), 5)

    def test_correct_pagination_on_second_page(self) -> None:
        create_sites(self.customer)
        response = self.client.get(SITE_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["site_list"]), 3)
