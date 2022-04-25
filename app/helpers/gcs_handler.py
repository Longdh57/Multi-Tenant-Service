import logging
from datetime import datetime, timedelta

from google.cloud import storage
from slugify import slugify

from app.core import error_code, message
from app.core.config import settings
from app.helpers.exception_handler import CustomException

logger = logging.getLogger()


class StorageAbstract(object):

    def presigned_get_object(self, bucket_name, object_name):
        pass

    def make_bucket(self) -> str:
        pass

    def presigned_get_object(self, bucket_name, object_name):
        pass

    def check_file_name_exists(self, bucket_name, file_name):
        pass

    def put_object(self, file_data, file_name, content_type):
        pass

    def normalize_file_name(self, file_name):
        pass


class GoogleCloudHandler(StorageAbstract):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """

        if not GoogleCloudHandler.__instance:
            GoogleCloudHandler.__instance = GoogleCloudHandler()
        return GoogleCloudHandler.__instance

    def __init__(self):
        self.client = storage.Client.from_service_account_info(
            settings.GOOGLE_APPLICATION_CREDENTIALS_CONTENT)
        self.bucket_name = settings.GOOGLE_BUCKET_NAME
        self.bucket = storage.Bucket(client=self.client, name=self.bucket_name)

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7)
        )
        return url

    def check_file_name_exists(self, file_name):
        try:
            # blob = storage.Blob(bucket=self.bucket,
            #                     name=file_name)
            # print(blob.)
            # a = self.bucket.get_blob(file_name)
            # print(a)
            return False
        except Exception as e:
            logger.debug(e)
            return False

    def download_file_name(self, filename):
        blob = storage.Blob(name=filename, bucket=self.bucket)
        file = blob.download_as_bytes(client=self.client)
        return file

    def get_object(self, filename):
        return self.download_file_name(filename=filename)

    def put_object(self, file_data, file_name, content_type):
        try:

            file_name = self.normalize_file_name(file_name)
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            # while self.check_file_name_exists(bucket_name=self.bucket_name, file_name=object_name):
            #     random_prefix = random.randint(1, 1000)
            #     object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"
            blob = storage.Blob(name=object_name, bucket=self.bucket)
            blob.upload_from_file(file_obj=file_data,
                                  content_type=content_type)
            # url = self.presigned_get_object(
            #     bucket_name=self.bucket_name, object_name=object_name)
            data_file = {
                'bucket_name': self.bucket_name,
                'file_name': object_name,
                'url': object_name
            }
            return data_file
        except Exception as e:
            raise Exception(e)

    def normalize_file_name(self, file_name):
        try:
            file_name = " ".join(file_name.strip().split())
            file_ext = file_name.split('.')[-1]
            file_name = ".".join(file_name.split('.')[:-1])
            file_name = slugify(file_name)
            file_name = file_name[:100]
            file_name = file_name + '.' + file_ext
            return file_name
        except Exception as e:
            logger.error(str(e))
            raise CustomException(
                http_code=400, code=error_code.ERROR_046_STANDARDIZED, message=message.MESSAGE_046_STANDARDIZED)
