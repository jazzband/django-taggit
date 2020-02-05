from django.conf.urls import url

from .views import TagAutocomplete

urlpatterns = [
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete', ),
]



