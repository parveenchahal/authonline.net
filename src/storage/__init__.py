from ._abstract_storage import Storage
from common.key_vault import KeyVaultSecret as _KeyVaultSecret
from .cosmos import CosmosContainerHandler as _CosmosContainerHandler, CosmosClientBuilderFromKeyvaultSecret as _CosmosClientBuilderFromKeyvaultSecret
from datetime import timedelta

def create_cosmos_container_handler(
    database_name: str,
    container_name: str,
    cache_timeout: timedelta,
    key_vault_secret: _KeyVaultSecret):
    client_builder = _CosmosClientBuilderFromKeyvaultSecret(key_vault_secret)
    cosmos_container_handler = _CosmosContainerHandler(database_name, container_name, client_builder, cache_timeout)
    return cosmos_container_handler