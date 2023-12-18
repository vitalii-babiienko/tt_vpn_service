from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicCustomerTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="test_customer",
            password="1qazcde3",
        )

    def test_login_required(self) -> None:
        response = self.client.get(
            reverse("vpn:customer-detail", kwargs={"pk": self.customer.id})
        )

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vpn/customers/1/"
        )


class PrivateCustomerTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="test_customer",
            password="1qazcde3",
        )
        self.client.force_login(self.customer)

    def test_view_exists_at_desired_location(self) -> None:
        response = self.client.get("/vpn/customers/1/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse("vpn:customer-detail", kwargs={"pk": self.customer.id})
        )

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse("vpn:customer-detail", kwargs={"pk": self.customer.id})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "vpn/customer_detail.html"
        )
