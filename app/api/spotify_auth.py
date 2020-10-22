import base64, json, requests, os, time


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
    access_token = None
    refresh_token = None
    expires_at = None

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
            self.refresh_token = response['refresh_token']
        self.access_token = response['access_token']
        self.expires_at = int(time.time()) + response['expires_in']
        print("ACCESS TOKEN IN AUTH: " + self.access_token)
        return self.access_token

    def refreshAuth(self, refresh_token, client_id, client_secret):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        post_refresh = requests.post(
            self.SPOTIFY_URL_TOKEN,
            data=body,
            headers=self.getHeaders(client_id, client_secret)
            )
        p_back = json.loads(post_refresh.text)

        return self.handleToken(p_back)

    def getUser(self):
        return self.getAuth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )

    def is_token_expired(self):
        now = int(time.time())
        return self.expires_at - now < 60
    
    def getUserTokens(self, code):
        return self.getToken(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )

    def getAccessToken(self):
        if self.access_token:
            if self.is_token_expired():
                return self.refreshAuth(
                    self.refresh_token,
                    self.CLIENT_ID,
                    self.CLIENT_SECRET
                )
            else:
                return self.access_token
        else:
            raise SpotifyAuthError({
                        "error":"missing_tokens",
                        "error_description":
                            "Access and refresh tokens must first be requested",
                    })


spotify_auth = SpotifyAuth()

