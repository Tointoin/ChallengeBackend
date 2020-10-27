from django.views.generic.base import RedirectView
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from app.api.spotify_auth import SpotifyAuth, getAccessToken

from app.api import serializer
from app.api.models import Artist, Album

import django_filters as filters
from django_filters.rest_framework import DjangoFilterBackend

from datetime import date, timedelta

import os, time


class SpotifyLoginView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return SpotifyAuth().getUser()


@api_view(['GET'])
def SpotifyCallbackView(request):
    code = request.query_params['code']
    response = SpotifyAuth().getUserTokens(code)
    cache.set('access_token', response['access_token'])
    cache.set('refresh_token', response['refresh_token'])
    cache.set('expires_at', int(time.time()) + response['expires_in'])
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def TokenAccessView(request):
    data = getAccessToken()
    return Response(data=data, status=status.HTTP_200_OK)


def filter_days_since_release(queryset, name, value):
    if not value:
        value = 7
    return queryset.filter(
        albums__release_date__gte=date.today()-timedelta(days=int(value))
        )


class NewReleaseArtistFilter(filters.FilterSet):
    # Fields
    is_available_in_france = filters.BooleanFilter(
        field_name="albums__available_in_france",
        )
    max_days_since_release = filters.NumberFilter(
        field_name="albums__release_date",
        method=filter_days_since_release
    )
    album_type = filters.ChoiceFilter(
        field_name="albums__album_type",
        choices=(
        ("album","album"),
        ("single","single"),
        ("compilation","compilation")
        )
    )

    class Meta:
        model = Artist
        fields = [
            "is_available_in_france", "album_type",
            "max_days_since_release",
            ]


class NewReleaseArtistView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = serializer.ArtistSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NewReleaseArtistFilter


