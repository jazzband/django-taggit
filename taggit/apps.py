from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(BaseConfig):
    name = 'taggit'
    verbose_name = _('Taggit')
