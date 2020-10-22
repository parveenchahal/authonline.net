from common import Model
from dataclasses import dataclass

@dataclass
class RoleAssignmentModel(Model):
    role_name: str
