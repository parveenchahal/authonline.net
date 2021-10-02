from common import Controller
from common.crypto import CertificateHandler
from common.utils import encode_base64, bytes_to_string
from common import http_responses

class PublicCertificatesController(Controller):

    _certificate_handler: CertificateHandler

    def __init__(self, logger, certificate_handler: CertificateHandler):
        super().__init__(logger)
        self._certificate_handler = certificate_handler

    def get(self):
        try:
            cert_list = self._certificate_handler.get()
            return [bytes_to_string(encode_base64(x.certificate)) for x in cert_list], 200
        except Exception as e:
            self._logger.exception(e)
            return http_responses.InternalServerErrorResponse()