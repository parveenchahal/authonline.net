from common.utils import encode_base64, string_to_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from crypto.certificate_handler import CertificateHandler
class RSASignature(object):

    __certificate_handler: CertificateHandler

    def __init__(self, certificate_handler: CertificateHandler):
        self.__certificate_handler = certificate_handler

    def get_signature(self, data) -> str:
        key = self.__certificate_handler.get()[0].private_key
        signer = PKCS1_v1_5.new(RSA.importKey(key))
        h = SHA256.new(string_to_bytes(data))
        sig = signer.sign(h)
        return encode_base64(sig)