from django.views.generic.base import RedirectView
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.api.spotify_auth import SpotifyAuth, getAccessToken


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


@api_view(['GET'])
def RefreshTokenView(request):
    response = SpotifyAuth().refreshAuth(cache.get('refresh_token'))
    access_token = response['access_token']
    cache.set('access_token', access_token)
    expires_at = int(time.time()) + response['expires_in']
    cache.set('expires_at', expires_at)
    return Response(data=access_token, status=status.HTTP_200_OK)



