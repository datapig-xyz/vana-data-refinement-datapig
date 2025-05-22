import json
import logging
import os
import requests
from refiner.config import settings
import time
import random

PINATA_FILE_API_ENDPOINT = "https://api.quicknode.com/ipfs/rest/v1/s3/put-object"
PINATA_JSON_API_ENDPOINT = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

def upload_json_to_ipfs(data):
    """
    Uploads JSON data to IPFS using Pinata API.
    :param data: JSON data to upload (dictionary or list)
    :return: IPFS hash
    """
    if not settings.PINATA_API_KEY or not settings.PINATA_API_SECRET:
        raise Exception("Error: Pinata IPFS API credentials not found, please check your environment variables")

    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": settings.PINATA_API_KEY,
        "pinata_secret_api_key": settings.PINATA_API_SECRET
    }

    try:
        response = requests.post(
            PINATA_JSON_API_ENDPOINT,
            data=json.dumps(data),
            headers=headers
        )
        response.raise_for_status()

        result = response.json()
        logging.info(f"Successfully uploaded JSON to IPFS with hash: {result['IpfsHash']}")
        return result['IpfsHash']

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while uploading JSON to IPFS: {e}")
        raise e

def upload_file_to_ipfs(file_path=None):
    """
    Uploads a file to IPFS using quicknode API (https://pinata.cloud/)
    :param file_path: Path to the file to upload (defaults to encrypted database)
    :return: IPFS hash
    """
    if file_path is None:
        # Default to the encrypted database file
        file_path = os.path.join(settings.OUTPUT_DIR, "db.libsql.pgp")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if not settings.QUICKNODE_API_KEY:
        raise Exception("Error: quicknode IPFS API credentials not found, please check your environment variables")

    headers = {
        'x-api-key': settings.QUICKNODE_API_KEY,
    }

    try:
        url = "https://api.quicknode.com/ipfs/rest/v1/s3/put-object"
        uniqueKey = f"datapig-encrypt-{int(time.time() * 1000)}-{int(random.random() * 10000)}"
        payload = {'Key': uniqueKey,  'ContentType': 'text/javascript'}
        files=[
            ('Body',('11111',open(file_path,'rb'),'text/javascript'))
        ]
        headers = {
        'x-api-key': settings.QUICKNODE_API_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # with open(file_path, 'rb') as file:
        #     files = {
        #         'file': file
        #     }
        #     response = requests.post(
        #         PINATA_FILE_API_ENDPOINT,
        #         files=files,
        #         headers=headers
        #     )
        
        response.raise_for_status()
        result = response.json()
        logging.info(f"Successfully uploaded file to IPFS with hash: {result['pin']['cid']}")
        return result['pin']['cid']

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while uploading file to IPFS: {e}")
        raise e

# Test with: python -m refiner.utils.ipfs
if __name__ == "__main__":
    ipfs_hash = upload_file_to_ipfs()
    print(f"File uploaded to IPFS with hash: {ipfs_hash}")
    print(f"Access at: https://ipfs.vana.org/ipfs/{ipfs_hash}")
    
    ipfs_hash = upload_json_to_ipfs()
    print(f"JSON uploaded to IPFS with hash: {ipfs_hash}")
    print(f"Access at: https://ipfs.vana.org/ipfs/{ipfs_hash}")