echo "Fetching access token for keyvault..."
identity_url="http://aad-identity-service.default:2424/$AAD_IDENTITY_TENANT?client_id=$AAD_IDENTITY_CLIENTID&secret=$AAD_IDENTITY_SECRET"
identity_url="$identity_url&resource=https://vault.azure.net"
accesstoken=$(curl -sS $identity_url | jq -r '.access_token')

secret_name="google-oauth-secret"
echo "Fetching secret $secret_name from keyvault..."
data=$(curl -sS "https://pckv1.vault.azure.net/secrets/$secret_name?api-version=2016-10-01" -H "Authorization: Bearer $accesstoken" | jq -r '.value')
mkdir /etc/secrets
echo $data | base64 -d > /etc/secrets/google-oauth-secret

export GOOGLE_OAUTH_SECRET_FILE_PATH="/etc/secrets/google-oauth-secret"

export FLASK_APP=session.app.py
export FLASK_ENV=production

flask run -h 0.0.0.0 -p 5000