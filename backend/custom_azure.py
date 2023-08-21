# custom_azure_storage.py
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'casquettedzstorage'
    account_key = 'AV8BwjeS5HtYNtJAityL827+LQH1hsjMr3VOXlPZDz8xhYlcJWCd3iiPuiMe52QmiYau8rVECszJ+ASt0KwkVA=='  # Or use AZURE_SAS_TOKEN for more secure access
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'casquettedzstorage'
    account_key = 'AV8BwjeS5HtYNtJAityL827+LQH1hsjMr3VOXlPZDz8xhYlcJWCd3iiPuiMe52QmiYau8rVECszJ+ASt0KwkVA=='  # Or use AZURE_SAS_TOKEN for more secure access
    azure_container = 'static'
    expiration_secs = None
