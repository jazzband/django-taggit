from django.shortcuts import render

from sample_taggit.models import Post


def index_view(request):
    return render(request, "index.html", {"posts": Post.objects.all()})
