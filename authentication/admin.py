from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from authentication.models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'uuid',
    )
    readonly_fields = (
        'uuid',
        'id',
    )

    fieldsets = (
        (None, {
           'fields': (
               'name',
               'uuid',
           )
        }),
        (_('Personal info'), {
            'fields': (
                'public_key',
            ),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'date_joined',
            ),
        }),
    )
