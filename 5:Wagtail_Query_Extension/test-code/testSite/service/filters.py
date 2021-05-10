from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.filters import BaseFilterBackend
from taggit.managers import TaggableManager


class ServiceFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        print(request)

        # Filter tags
        # Ages > and <
        return queryset