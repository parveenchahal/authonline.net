import uuid
from datetime import datetime, timedelta
from session.models import Session
from access_token_payload.models.access_token_payload_model import AccessTokenPayloadModel


def generate_access_token_payload_using_session(session: Session, remote_addr: str, expiry: timedelta = timedelta(hours=1)) -> AccessTokenPayloadModel:
    access_token = AccessTokenPayloadModel()
    access_token.aud = session.resource
    access_token.iss = "https://authonline.net"
    access_token.scp = 'user_impersonation'
    access_token.sub = session.sid
    access_token.username = session.username
    access_token.amr = session.amr
    access_token.remote_addr = remote_addr

    now_utc = int(datetime.utcnow().timestamp())
    exp = now_utc + int(expiry.total_seconds())

    access_token.iat = now_utc
    access_token.nbf = now_utc
    access_token.exp = exp

    access_token.jti = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{session.sid} + {str(exp)}"))

    return access_token