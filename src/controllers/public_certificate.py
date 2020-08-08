from controllers import Controller
from crypto.certificate_handler import CertificateHandler
from common.utils import encode_base64
from error_responses import InternalServerError

class PublicCertificate(Controller):

    __certificate_handler: CertificateHandler

    def __init__(self, logger, certificate_handler: CertificateHandler):
        super().__init__(logger)
        self.__certificate_handler = certificate_handler

    def get(self):
        try:
            cert_list = self.__certificate_handler.get()
            return [encode_base64(x.certificate) for x in cert_list], 200
        except Exception as e:
            self._logger.exception(e)
            return InternalServerError()