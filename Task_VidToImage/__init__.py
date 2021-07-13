import logging

from azure.storage import blob
import cv2
import os
from azure.storage.blob import ContainerClient
from skimage.metrics import structural_similarity as ssim
import numpy as np

def main(VidToImageAF: dict) -> str:
    logging.info(" VidToImage dict ---------> %s",VidToImageAF)
    account_name= os.getenv('ACCOUNT_NAME')
    container_sas_url=f"https://{account_name}.blob.core.windows.net/images?{VidToImageAF['sasToken']}"
    container_client =  ContainerClient.from_container_url(container_sas_url)
    outfolderName = VidToImageAF['blobName'].split("/")[-1][:-4]
    vidcap = cv2.VideoCapture(VidToImageAF['tmpBlobName'])
    width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    dim = (int(height),int(width))
    previousImage = np.zeros((int(height),int(width),3), dtype=np.uint8)
    previousImage = cv2.resize(previousImage,dim,interpolation = cv2.INTER_AREA)
    count = 0
    while vidcap.isOpened():
            success, image = vidcap.read()
            if success:
                # Save files to local disk for testing
                # cv2.imwrite("frame%d.jpg" % count, image)
                # Save files Blob Storage
                cv2.imencode(".jpeg", image)
                currentImage = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
                score =  isAlotSimilarScore(currentImage,previousImage)
                if (score <= 0.95):
                    byteImage = image.tobytes()
                    blobName=f"{outfolderName}/frame-{count}.jpeg"
                    container_client.upload_blob(name=blobName,data=byteImage,overwrite=True)
                count += 1
                previousImage = currentImage
    #  Remove downloaded vid file
    os.remove(VidToImageAF['tmpBlobName'])
    return f"Hello {VidToImageAF}!"

def isAlotSimilarScore(currentImage,previousImage) : 
    currentImageGray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)
    previousImageGray = cv2.cvtColor(previousImage, cv2.COLOR_BGR2GRAY)
    score = ssim(previousImage,currentImage,multichannel=True)
    return score