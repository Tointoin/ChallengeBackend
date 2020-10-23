from django.core.management.base import BaseCommand

from app.api.models import Album, Artist


class Command(BaseCommand):
    help = "Remove all Artists and Albums in DB"

    def handle(self, *args, **options):
        for artist in Artist.objects.all():
            artist.delete()
        
        for album in Album.objects.all():
            album.delete()


        