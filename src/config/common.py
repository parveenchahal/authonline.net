import os
from datetime import timedelta

BaseUrl = "https://authonline.net/"

KeyVaultName = "pckv1"

SigningCertificateName = "authonline-token-signing"

CosmosDbConnectionStrings = "pc-cosmos-db-connection-string"

DatebaseName = "authonline"

SessionExpiry: timedelta = timedelta(hours=1)
RefreshSessionAfterInterval = timedelta(minutes=1)

def init():
    pass