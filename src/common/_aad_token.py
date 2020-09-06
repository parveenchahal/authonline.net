from requests import get as _http_get
from common.utils import parse_json

class AADToken(object):

    _auth_url: str = 'http://aad-identity-service.default:2424/{0}?client_id={1}&secret={2}&resource={3}'

    def __init__(self, client_id: str, secret: str, resource: str, tenant: str = 'common'):
        self._auth_url = self._auth_url.format(tenant, client_id, secret, resource)
    
    @property
    def access_token(self):
        res = _http_get(self._auth_url)
        return parse_json(res.text)["access_token"]
