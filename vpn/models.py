from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Customer(AbstractUser):
    bio = models.TextField(default="Here you can add some bio about you ;)")

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> str:
        return reverse("vpn:customer-detail", kwargs={"pk": self.id})


class Site(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sites",
    )
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("vpn:site-detail", kwargs={"pk": self.id})


class Statistic(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="data",
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="data",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    sent_data = models.IntegerField(default=0)
    received_data = models.IntegerField(default=0)
