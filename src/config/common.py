import os
from datetime import timedelta

BaseUrl = "https://authonline.net/"

SigningCertificateUri = "https://pckv1.vault.azure.net/secrets/authonline-token-signing?api-version=2016-10-01"

KeyVaultAuthTokenUri = None

SessionExpiry: timedelta = timedelta(days=1)

def init():
    global KeyVaultAuthTokenUri
    AAD_IDENTITY_TENANT = os.environ['AAD_IDENTITY_TENANT']
    AAD_IDENTITY_CLIENTID = os.environ['AAD_IDENTITY_CLIENTID']
    AAD_IDENTITY_SECRET = os.environ['AAD_IDENTITY_SECRET']
    KeyVaultAuthTokenUri=f"http://localhost:2424/{AAD_IDENTITY_TENANT}?client_id={AAD_IDENTITY_CLIENTID}&secret={AAD_IDENTITY_SECRET}&resource=https://vault.azure.net"