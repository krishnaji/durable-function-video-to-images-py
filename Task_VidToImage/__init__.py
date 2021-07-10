import logging

from azure.storage import blob
import cv2
import os
from azure.storage.blob import ContainerClient

def main(VidToImageAF: dict) -> str:
    logging.info(" VidToImage dict ---------> %s",VidToImageAF)
    account_name= os.getenv('ACCOUNT_NAME')
    container_sas_url=f"https://{account_name}.blob.core.windows.net/images?{VidToImageAF['sasToken']}"
    container_client =  ContainerClient.from_container_url(container_sas_url)
    outfolderName = VidToImageAF['blobName'].split("/")[-1][:-4]
    count = 0
    vidcap = cv2.VideoCapture(VidToImageAF['tmpBlobName'])
    while vidcap.isOpened():
            success, image = vidcap.read()
            if success:
                # Save files to local disk for testing
                # cv2.imwrite("frame%d.jpg" % count, image)
                # Save files Blob Storage
                cv2.imencode(".jpeg", image)
                byteImage = image.tobytes()
                blobName=f"{outfolderName}/frame-{count}.jpeg"
                container_client.upload_blob(name=blobName,data=byteImage,overwrite=True)
                count += 1
    #  Remove downloaded vid file
    os.remove(VidToImageAF['tmpBlobName'])
    return f"Hello {VidToImageAF}!"
