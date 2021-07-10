import logging
import json
from azure.storage.blob import BlobClient
import uuid
def main(downloadBlobAF: dict) -> str:
   #  blobOptions = (json.loads(downloadBlobAF))
    blob_client = BlobClient.from_blob_url(blob_url=downloadBlobAF['sas_uri'])
    tmpBlobName= str(uuid.uuid4())
    with open(tmpBlobName, "wb") as tmpblob:
       download_stream = blob_client.download_blob()
       tmpblob.write(download_stream.readall())
    dict = {}
    dict['sas_uri'] = downloadBlobAF['sas_uri']
    dict['tmpBlobName'] = tmpBlobName
    dict['blobName'] = downloadBlobAF['blobname']
    dict['sasToken'] = downloadBlobAF['sasToken']
    return  dict



