from abc import abstractmethod
from typing import List
from crypto.models.certificate import Certificate

class CertificateHandler(object):
    
    @abstractmethod
    def get(self) -> List[Certificate]:
        raise NotImplementedError()