from rest_framework import serializers
from app.api.models import Album, Artist


class AlbumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Album
        fields = [
            'title', 'href', 'release_date',
            'available_in_france',  'uuid', 'album_type',
            ]
        ordering = ['-release_date']


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ['name', 'albums']
