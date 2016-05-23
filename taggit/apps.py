from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig as BaseConfig


class AppConfig(BaseConfig):
    name = 'taggit'
    verbose_name = _('Taggit')
