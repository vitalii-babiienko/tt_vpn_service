from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from vpn.models import Customer, Statistic, Site


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "bio",
                    )
                }
            ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "bio",
                    )
                },
            ),
        )
    )


admin.site.register(Site)
admin.site.register(Statistic)
