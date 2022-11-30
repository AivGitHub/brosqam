from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class KeyValidator:
    message = _('Allowed algorithms are: %(key_types)s')
    code = 'invalid'
    key_types = ('public', 'private')

    def __init__(self, key_type: str = 'public', allowed_algorithms: list = None, message: str = None) -> None:
        self.key_type = key_type

        if allowed_algorithms is None:
            allowed_algorithms = []
        else:
            allowed_algorithms = [
                allowed_extension.lower() for allowed_extension in allowed_algorithms
            ]

        self.allowed_algorithms = allowed_algorithms

        if message is not None:
            self.message = message

    def __call__(self, value) -> None:
        if self.allowed_algorithms and not self.is_valid(value):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'key_types': ', '.join(self.allowed_algorithms),
                    'value': value,
                }
            )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.allowed_algorithms == other.allowed_algorithms
            and self.message == other.message
            and self.code == other.code
            and self.key_type == other.key_type
        )

    def is_valid(self, value) -> bool:
        # TODO: validate key
        return True


validate_public_key = KeyValidator()
