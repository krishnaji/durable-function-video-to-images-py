import logging
import os
import json
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_account_sas, AccountSasPermissions ,ResourceTypes

def main(options: str) -> str:
    blobOptions = (json.loads(options))
    container = blobOptions['container']
    blob =  blobOptions['blob']
    account_name= os.getenv('ACCOUNT_NAME')
    account_key= os.getenv('ACCOUNT_KEY')

    sas_token = generate_account_sas(
    account_name= account_name,
    account_key= account_key,
    resource_types=ResourceTypes(object=True),
    # container_name= container,
    # blob_name = blob,
    permission=AccountSasPermissions(read=True,write=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)
    sas_uri = f"https://{account_name}.blob.core.windows.net/{container}/{blob}?{sas_token}"
    logging.info('Task_GetSASUri---------------> %s',sas_uri)
    dict = {}
    dict['sas_uri'] = sas_uri
    dict['blobname'] = blob
    dict['container'] = container
    dict['sasToken'] = sas_token
    return dict