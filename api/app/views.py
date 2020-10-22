from django.views.generic.base import RedirectView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.app.spotify_auth import spotify_auth

import os


class SpotifyLoginView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return spotify_auth.getUser()


@api_view(['GET'])
def SpotifyCallbackView(request):
    if 'code' in request.query_params.keys():
        code = request.query_params['code']
        global spotify_auth
        spotify_auth.getUserTokens(code)
        print("ACCESS TOKEN IN VIEWS: " + spotify_auth.getAccessToken())
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def TokenAccessView(request):
    global spotify_auth
    data = spotify_auth.getAccessToken()
    print(spotify_auth.__dict__)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def RefreshTokenView(request):
    global spotify_auth
    data = spotify_auth.refreshAuth(
        spotify_auth.refresh_token,
        spotify_auth.CLIENT_ID,
        spotify_auth.CLIENT_SECRET
        )
    return Response(data=data, status=status.HTTP_200_OK)



