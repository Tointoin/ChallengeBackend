from django.contrib import admin
from app.api import models


class HasBeenCreatedByInline(admin.TabularInline):
    model = models.Album.artists.through

class ArtistAdmin(admin.ModelAdmin):
    model = models.Artist
    readonly_fields = ('uuid',)
    inlines = [
        HasBeenCreatedByInline,
    ]
    list_display = ['name', 'uuid']
    search_fields = ['name', 'uuid', 'albums__title']


class AlbumAdmin(admin.ModelAdmin):
    model = models.Album
    readonly_fields = ('uuid',)
    list_display = ['title', 'release_date', 'album_type', 'available_in_france']
    search_fields = ['title', 'release_date', 'artists__name', 'album_type', 'available_in_france']


admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Album, AlbumAdmin)