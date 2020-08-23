import os
from datetime import timedelta

BaseUrl = "https://authonline.net/"

KeyVaultName = "pckv1"

SigningCertificateName = "authonline-token-signing"

CosmosDbConnectionStrings = "pc-cosmos-db-connection-string"

DatebaseName = "authonline"

SessionExpiry: timedelta = timedelta(days=60)
RefreshSessionAfterInterval = timedelta(minutes=2)

def init():
    pass