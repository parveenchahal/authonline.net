from .abstract_controller import Controller
from crypto.certificate_handler import CertificateHandler
from common.utils import encode_base64
import http_responses

class PublicCertificates(Controller):

    __certificate_handler: CertificateHandler

    def __init__(self, logger, certificate_handler: CertificateHandler):
        super().__init__(logger)
        self.__certificate_handler = certificate_handler

    def get(self):
        try:
            cert_list, _ = self.__certificate_handler.get()
            return [encode_base64(x.certificate) for x in cert_list], 200
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()