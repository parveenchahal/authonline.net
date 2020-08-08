import urllib.parse
import config.common as common

ClientId = "789522065274-dms9tf5tgg8n7emhqfidttnsj4qiq5ae.apps.googleusercontent.com"
RedirectUri = None
LoginUrl = None


def init():
    global LoginUrl, RedirectUri

    RedirectUri = urllib.parse.urljoin(common.BaseUrl, "googlesignin/auth")
    LoginUrl = f"https://accounts.google.com/signin/oauth/identifier?redirect_uri={RedirectUri}&response_type=code&client_id={ClientId}&scope=email%20profile&access_type=offline&prompt=select_account"
