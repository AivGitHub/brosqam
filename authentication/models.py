import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from retry import retry

from authentication.exceptions import AlreadyExists
from authentication.validators import validate_public_key


@retry(AlreadyExists, tries=5)
def generate_uuid():
    uid = uuid.uuid4()

    try:
        Business.objects.get(uuid=uid)
    except Business.DoesNotExist:
        return uid

    raise AlreadyExists()


class Business(models.Model):
    uuid = models.UUIDField(
        _('Business identifier'),
        default=generate_uuid,
        unique=True,
        editable=False,
        null=False,
        blank=False
    )
    name = models.CharField(
        _('Name'),
        max_length=256,
        null=False,
        blank=False
    )
    public_key = models.TextField(
        _('Public key'),
        max_length=1024,
        null=True,
        blank=True,
        validators=[validate_public_key]
    )
    date_joined = models.DateTimeField(
        _('Date joined'),
        default=timezone.now
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this business should be treated as active. '
            'Unselect this instead of deleting businesses.'
        ),
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'business'
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')

    def __str__(self):
        return '%s - %s' % (self.name, self.uuid)
