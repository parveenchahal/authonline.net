from datetime import timedelta

BaseUrl = 'https://apis.authonline.net/'

AuthonlineClientId = '10a06848-a289-4c83-9ada-0532ce67473b'

KeyVaultName = "pckv1"

SigningCertificateName = "authonline-token-signing"

CosmosDbConnectionStrings = "pc-cosmos-db-connection-string"

CosmosOfferThroughput = 400

DatebaseName = "authonline"

SessionExpiry: timedelta = timedelta(days=60)
RefreshSessionAfterInterval = timedelta(minutes=5)

def init():
    pass