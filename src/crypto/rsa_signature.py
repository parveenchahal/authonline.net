from common.utils import encode_base64, string_to_bytes, to_json_string, encode_base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from crypto.certificate_handler import CertificateHandler
class RSASignature(object):

    __certificate_handler: CertificateHandler

    def __init__(self, certificate_handler: CertificateHandler):
        self.__certificate_handler = certificate_handler

    def get_signature(self, data) -> [str, str]:
        key = self.__certificate_handler.get()[0].private_key
        signer = PKCS1_v1_5.new(RSA.importKey(key))
        h = SHA256.new(string_to_bytes(data))
        sig = signer.sign(h)
        header =  encode_base64(to_json_string({
            "alg": "SHA256"
        }), remove_padding=True)
        return header, encode_base64(sig, remove_padding=True)