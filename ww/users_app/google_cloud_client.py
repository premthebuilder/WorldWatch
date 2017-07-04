from google.cloud import storage
from google.cloud.storage.blob import Blob
from django.contrib.gis.maps import google

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

class GoogleStoreClient:
    def __init__(self, bucket_name):
        self.storage_client = storage.Client(project = "yuga-171020")
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)
        except google.cloud.exceptions.NotFound:
            print("Sorry, that bucket does not exist")
        self.encryption_key = 'c7f32af42e45e85b9848a6a14dd2a8f6'
        self.blob = Blob('secure-data', self.bucket, encryption_key=self.encryption_key)
        
    def create_upload_session_url(self):
        upload_session_url = self.blob.create_resumable_upload_session()
        logger.info("Created upload session url: " + upload_session_url)
        return upload_session_url
        
if __name__ == "__main__":
    client = GoogleStoreClient("yuga-171020.appspot.com")       
    print(client.create_upload_session_url())
    