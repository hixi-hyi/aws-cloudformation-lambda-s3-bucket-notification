from cfnprovider import CustomResourceProvider, get_logger, policy
import boto3
import os
logger = get_logger(__name__)
env = os.environ


class S3BucketNotificationConfiguration(CustomResourceProvider):
    def init(self):
        self._bucket = self.get('Bucket')
        self._notification_configuration = self.get('NotificationConfiguration')

        self._s3 = boto3.client('s3')
        self.response.physical_resource_id = self.id
        self.response.set_data('Bucket', self._bucket)

    @property
    def id(self):
        return "{}".format(self._bucket)

    def default_deletion_policies(self):
        return ['Delete']

    def put_bucket_notification_configuration(self):
        self._s3.put_bucket_notification_configuration(
            Bucket=self._bucket,
            NotificationConfiguration=self._notification_configuration,
        )

    def delete_bucket_notification_configuration(self):
        self._s3.put_bucket_notification_configuration(
            Bucket=self._bucket,
            NotificationConfiguration={},
        )

    def create(self, policies):
        self.put_bucket_notification_configuration()

    def update(self, policies):
        self.put_bucket_notification_configuration()

    def delete(self, policies):
        try:
            self.delete_bucket_notification_configuration()
        except Exception as e:
            if policies.has('IgnoreError'):
                return
            raise e


def handler(event, context):
    c = S3BucketNotificationConfiguration(event, context)
    c.handle()
