from django.conf.urls import patterns

from taggit.views import TaggedObjectList
from .models import Food


urlpatterns = patterns('',
    (r'^tagged/(?P<slug>[\w+]+)/$', TaggedObjectList.as_view(model=Food)),
)
