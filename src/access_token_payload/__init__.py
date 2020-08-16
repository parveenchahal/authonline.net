import uuid
from datetime import datetime, timedelta
from session.models import Session
from .models.access_token_payload_model import AccessTokenPayloadModel
import config.common as _config


def generate_access_token_payload_using_session(session: Session, remote_addr: str, expiry: timedelta = timedelta(hours=1)) -> AccessTokenPayloadModel:
    access_token = AccessTokenPayloadModel()
    access_token.aud = session.res
    access_token.iss = _config.BaseUrl
    access_token.scp = 'user_impersonation'
    access_token.sub = session.sid
    access_token.usr = session.usr
    access_token.amr = session.amr
    access_token.remote_addr = remote_addr

    now_utc = int(datetime.utcnow().timestamp())
    exp = now_utc + int(expiry.total_seconds())

    access_token.iat = now_utc
    access_token.nbf = now_utc
    access_token.exp = exp

    access_token.jti = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{session.sid} + {str(exp)}"))

    return access_token