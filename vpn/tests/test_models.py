from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from vpn.models import Site


class CustomerModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="test_customer",
            password="1qazcde3",
            first_name="Test First",
            last_name="Test Last",
        )
        self.client.force_login(self.customer)

    def test_customer_str(self) -> None:
        self.assertEquals(
            str(self.customer),
            f"{self.customer.username} "
            f"({self.customer.first_name} {self.customer.last_name})"
        )

    def test_customer_get_absolute_url(self) -> None:
        self.assertEquals(
            self.customer.get_absolute_url(),
            "/vpn/customers/1/",
        )

    def test_update_customer(self) -> None:
        new_bio = "updated bio"
        response = self.client.post(
            reverse("vpn:customer-update", kwargs={"pk": self.customer.id}),
            data={"bio": new_bio}
        )
        self.customer.refresh_from_db()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.customer.bio, new_bio)


class SiteModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="test_customer",
            password="1qazcde3",
        )
        self.client.force_login(self.customer)
        Site.objects.create(
            user=self.customer,
            name="test name",
            url="https://test.ua/",
        )

    def test_site_str(self) -> None:
        site = Site.objects.get(id=1)

        self.assertEquals(
            str(site),
            f"{site.name}",
        )

    def test_site_get_absolute_url(self) -> None:
        site = Site.objects.get(id=1)

        self.assertEquals(
            site.get_absolute_url(),
            "/vpn/sites/1/",
        )

    def test_update_site(self) -> None:
        site = Site.objects.create(
            user=self.customer,
            name="test name old",
            url="https://test.ua/",
        )
        new_name = "test name updated"
        response = self.client.post(
            reverse("vpn:site-update", kwargs={"pk": site.id}),
            data={"name": new_name}
        )

        self.assertEquals(response.status_code, 200)

    def test_delete_site(self) -> None:
        site = Site.objects.create(
            user=self.customer,
            name="test name del",
            url="https://test.ua/",
        )
        response = self.client.post(
            reverse("vpn:site-delete", kwargs={"pk": site.id})
        )

        self.assertEquals(response.status_code, 302)
        self.assertFalse(
            Site.objects.filter(id=site.id).exists()
        )
