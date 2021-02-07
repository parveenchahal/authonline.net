import os
from datetime import timedelta

BaseUrl = "https://authonline.pchahal.com/"

KeyVaultName = "pckv1"

SigningCertificateName = "authonline-token-signing"

CosmosDbConnectionStrings = "pc-cosmos-db-connection-string"

CosmosOfferThroughput = 400

DatebaseName = "authonline"

SessionExpiry: timedelta = timedelta(days=60)
RefreshSessionAfterInterval = timedelta(minutes=2)

def init():
    pass