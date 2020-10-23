from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import date

import uuid


# Abstract models
class ReferencedOnSpotifyAPI(models.Model):
    href = models.URLField(
        _('href'),
        blank=False,
        max_length=1024,
        help_text=_(
            "A link to the Spotify Web API endpoint providing full details."
            )
        )
    
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['href'],
                name='Spotify API unicity for %(class)s'
                )
        ]

class UUID(models.Model):

    uuid = models.UUIDField(
        _('uuid'),
        default=uuid.uuid4,
        primary_key=True,
        blank=False,
        max_length=255,
        editable=False
        )

    class Meta:
        abstract = True


# Models in DB
class Artist(ReferencedOnSpotifyAPI, UUID):

    name = models.CharField(_('name'), blank=True, max_length=512)  

    def __str__(self):
        return self.name


class Album(ReferencedOnSpotifyAPI, UUID):

    class AlbumTypes(models.TextChoices):
        ALBUM = "album"
        SINGLE = "single"
        COMPILATION = "compilation"

    title = models.CharField(_('title'), blank=True, max_length=512)
    artists = models.ManyToManyField(
        'Artist',
        verbose_name=_('artists'),
        related_name=_('albums'),
        blank=True,
        help_text=_(
            "List of artists that have played on the album."
            )
        ) 
    album_type = models.CharField(
        _('album_type'),
        max_length=11,
        choices=AlbumTypes.choices,
        default=AlbumTypes.ALBUM,
        help_text=_(
            """The type of the album: one of “album”, “single”, or “compilation”."""
            )
    )
    available_in_france = models.BooleanField(
        _('available_in_france'),
        default=True,
    )
    release_date = models.DateField(
        _('Release_date'),
        default=date.today,
        editable=True,
        blank=False,
        help_text=_(
            "Release date of the album."
            )
    )

    def __str__(self):
        return self.title

