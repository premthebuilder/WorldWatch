import logging
import datetime
import base64
import hashlib

from django.contrib.gis.maps import google

from google.cloud import storage
from google.cloud.storage.blob import Blob
# from test.support import resource


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
    
    def construct_string_to_sign(self, http_method):
        md5_digest = ""
        content_type = 'image/png'
        expiry_time = str(13885344009999)
        resource_path = "yuga-171020.appspot.com/test.png"
        sign_string = (http_method
        +"\n"
        +md5_digest
        +"\n"
        +content_type
        +"\n"
        +expiry_time)
        return sign_string
    
    def sign_string(self):
        from oauth2client.service_account import ServiceAccountCredentials
        creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/aster/Downloads/Yuga-08262615e481.json")
        client_id = creds.service_account_email
        signature = creds.sign_blob(self.construct_string_to_sign("PUT"))[1]
        return signature
    
    def build_url(self):
        base_url = "https://storage.googleapis.com/yuga-171020.appspot.com/test.png"
        google_access_storage_id =  "admin-926@yuga-171020.iam.gserviceaccount.com"
        expiration = str(13885344009999)
#         signature = str(base64.b64encode(self.sign_string()))
        signature = hashlib.sha256(self.sign_string()).hexdigest()
        print(signature)
        print(base_url + "?GoogleAccessId=" + google_access_storage_id + "&Expires=" + expiration + "&Signature=" + signature)
        
    def generate_signed_url(self, blob_name, method):
        """Generates a signed URL for a blob.
        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """
        blob = self.bucket.blob(blob_name)
    
        url = blob.generate_signed_url(
            # This URL is valid for 1 hour
            expiration=datetime.timedelta(hours=1),
            # Allow GET requests using this URL.
            method='GET')
    
        print('The signed url for {} is {}'.format(blob.name, url))
        
if __name__ == "__main__":
    client = GoogleStoreClient("yuga-171020.appspot.com")       
#     print(client.create_upload_session_url())
#     print(client.generate_signed_url("yuga-171020.appspot.com/secure-data/1501716053019583"))
    print(client.build_url())
    