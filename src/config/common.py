import os

BaseUrl = "https://authonline.net/"

SigningCertificateUri = "https://pckv1.vault.azure.net/secrets/authonline-token-signing?api-version=2016-10-01"

KeyVaultAuthTokenUri = ""

def init():
    AAD_IDENTITY_TENANT = os.environ['AAD_IDENTITY_TENANT']
    AAD_IDENTITY_CLIENTID = os.environ['AAD_IDENTITY_CLIENTID']
    AAD_IDENTITY_SECRET = os.environ['AAD_IDENTITY_SECRET']
    KeyVaultAuthTokenUri=f"http://aad-identity-service.default:2424/{AAD_IDENTITY_TENANT}?client_id={AAD_IDENTITY_CLIENTID}&secret={AAD_IDENTITY_SECRET}&resource=https://vault.azure.net"