from django.core.management.base import BaseCommand
from app.api.spotify_auth import getAccessToken
import requests

# global spotify_auth


class Command(BaseCommand):
    help = 'Dummy command to test getting a working access token'
    SPOTIFY_URL_API_ME = "https://api.spotify.com/v1/me"

    def handle(self, *args, **options):
        params = {"access_token": getAccessToken()}
        print(requests.get(self.SPOTIFY_URL_API_ME, params=params).text)
        