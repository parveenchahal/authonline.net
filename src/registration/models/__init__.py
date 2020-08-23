from dataclasses import dataclass
from common.abstract_model import Model

@dataclass
class RegistrationDetails(Model):
    user_id: str
    client_id: str
    redirect_uri: str
    