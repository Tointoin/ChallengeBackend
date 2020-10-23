from django.core.management.base import BaseCommand

from app.api.spotify_auth import getAccessToken
from app.api.models import Album, Artist

import json, requests


class Command(BaseCommand):
    help = "Fetch new released albums from Spotify API and store them in database"
    SPOTIFY_URL_API_NEW_RELEASE = "https://api.spotify.com/v1/browse/new-releases"
    limit = 50 # maximum number of albums returned by Spotify API new release route

    def handleFetchedData(self, items):
        """store recieved new albums in DB"""
        for i in items:
            album, created = Album.objects.get_or_create(
                href=i['href'],
                title=i['name'],
                album_type=i['album_type'],
                available_in_france= 'FR' in i['available_markets'],
            )
            for a in i['artists']:
                artist, created = Artist.objects.get_or_create(
                    href=a['href'],
                    name=a['name']
                )
                if artist not in album.artists.all():
                    album.artists.add(artist)
                    album.save()
        

    def handle(self, *args, **options):
        params = {"access_token": getAccessToken(), 'limit': self.limit}
        response = json.loads(
            requests.get(self.SPOTIFY_URL_API_NEW_RELEASE, params=params).text
        )
        print('KOUKOU')
        self.handleFetchedData(response['albums']['items'])
        while response['albums']['next']:
            response = json.loads(
                requests.get(response['albums']['next'], params=params).text
            )
            self.handleFetchedData(response['albums']['items'])

        