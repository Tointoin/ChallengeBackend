from model_bakery.recipe import Recipe, related, foreign_key
from app.api.models import Artist, Album
from itertools import cycle
from datetime import date, timedelta


kari_job = Recipe(Artist, name="Kari Jobe")
comethazine = Recipe(Artist, name="Comethazine")
lee_brice = Recipe(Artist, name="Lee Brice")
fiji_blue = Recipe(Artist, name= "Fiji Blue")

album_fixture = Recipe(Album)

blessing = album_fixture.extend(
    title="The Blessing (Live)",
    album_type="album",
    artists=related("kari_job"),
    available_in_france=False,
    release_date=date.today()-timedelta(days=3)
    )

bawskee = album_fixture.extend(
    title="Bawskee 4",
    album_type="single",
    artists=related("comethazine"),
    release_date=date.today()-timedelta(days=7)
    
    )

memory = album_fixture.extend(
    title="The Blessing (Live)",
    album_type="single",
    artists=related("lee_brice"),
    release_date=date.today()-timedelta(days=3)
    )

affection = album_fixture.extend(
    title="Affection",
    album_type="album",
    artists=related("fiji_blue"),
    release_date=date.today()-timedelta(days=3)
    )
