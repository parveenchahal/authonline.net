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

    now_utc = datetime.utcnow()
    access_token.iat = int(now_utc.timestamp())
    access_token.nbf = int(now_utc.timestamp())
    e = now_utc + expiry
    access_token.exp = e.timestamp()

    access_token.jti = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{session.sid} + {str(e)}"))

    return access_token