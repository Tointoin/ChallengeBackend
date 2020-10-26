from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from django.contrib.auth.models import User

from app.api.spotify_auth import getAccessToken
from app.api import models

from model_bakery import baker


class SpotifyAuthenticationTestCase(APITestCase):
    def test_get_token_from_cache(self):
        self.assertTrue(getAccessToken())


class NewReleaseArtistViewSetTesCase(APITestCase):
    def setUp(self):
        self.bkari_job = baker.make_recipe("app.api.kari_job")
        self.comethazine = baker.make_recipe("app.api.comethazine")
        self.lee_brice = baker.make_recipe("app.api.lee_brice")
        self.fiji_blue = baker.make_recipe("app.api.fiji_blue")
        
        self.blessing = baker.make_recipe("app.api.blessing")
        self.bawskee = baker.make_recipe("app.api.bawskee")
        self.memory = baker.make_recipe("app.api.memory")
        self.affection = baker.make_recipe("app.api.affection")

        self.parameters = {
            "is_available_france":True,
            "days_since_release":4,
            "album_type":"single",
        }

        self.user = User.objects.create(username="admin")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_NewReleaseArtistViewSet(self):
        artist_list_url = reverse('artist-list')
        response = self.client.get(
            artist_list_url,
            data=self.parameters,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
