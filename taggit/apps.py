from django.apps import AppConfig as BaseConfig
from django.utils.translation import gettext_lazy as _


class TaggitAppConfig(BaseConfig):
    name = "taggit"
    verbose_name = _("Taggit")
