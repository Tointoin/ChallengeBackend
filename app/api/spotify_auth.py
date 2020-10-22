import base64, json, requests, os, time
from django.core.cache import cache

class SpotifyAuthError(Exception):
    """
    Attributes:
        response -- dict with an error and an error_description keys
    """
    
    def __init__(self, response):
        self.error = response["error"]
        self.description = response["error_description"]

    def __str__(self):
        return f"{self.error} error occured: {self.description}"


class SpotifyAuth(object):
    SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
    SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CALLBACK_URL = "http://localhost:5000/auth"
    SCOPE = "user-read-email user-read-private"

    def getAuth(self, client_id, redirect_uri, scope):
        return (
            f"{self.SPOTIFY_URL_AUTH}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            "&response_type=code"
        )

    def getHeaders(self, client_id, client_secret):
        encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        return {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        } 

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        post = requests.post(
            self.SPOTIFY_URL_TOKEN,
             params=body, 
             headers=self.getHeaders(client_id, client_secret)
             )
        return self.handleToken(json.loads(post.text))

    def handleToken(self, response):
        if "error" in response:
            raise SpotifyAuthError(response)
        # refresh token is absent of response while refreshing access token
        if "refresh_token" in response:
            keys = ["access_token", "expires_in", "refresh_token"]
        else:
            keys = ["access_token", "expires_in"]
        return {
            key: response[key]
            for key in keys
        }

    def refreshAuth(self, refresh_token):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        post_refresh = requests.post(
            self.SPOTIFY_URL_TOKEN,
            data=body,
            headers=self.getHeaders(self.CLIENT_ID, self.CLIENT_SECRET)
            )
        p_back = json.loads(post_refresh.text)

        return self.handleToken(p_back)

    def getUser(self):
        return self.getAuth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )
    
    def getUserTokens(self, code):
        return self.getToken(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )


def is_token_expired(expires_at):
    now = int(time.time())
    return expires_at - now < 60


def getAccessToken():
    access_token = cache.get('access_token')
    refresh_token = cache.get('refresh_token')
    expires_at = cache.get('expires_at')
    if access_token:
        if is_token_expired(expires_at):
            response = SpotifyAuth().refreshAuth(refresh_token)
            access_token = response['access_token']
            cache.set('access_token', access_token)
            expires_at = int(time.time()) + response['expires_in']
            cache.set('expires_at', expires_at)
            return access_token
        else:
            return access_token
    else:
        raise SpotifyAuthError({
                    "error":"missing_tokens",
                    "error_description":
                        "Access and refresh tokens must first be requested",
                })


