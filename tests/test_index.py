from unittest import TestCase
from moto import mock_s3
from src.index import S3BucketNotificationConfiguration
import cfntest
import boto3


def get_bucket_notification_configuration(bucket_name):
    return boto3.client('s3').get_bucket_notification_configuration(Bucket=bucket_name)


class TestScenario(TestCase):
    @mock_s3
    def test_default(self):
        bucket_name = 'test'
        lambda_arn = 'arn:aws:lambda:us-east-1:123456789012:function:my-function'
        s3 = boto3.client('s3')
        s3.create_bucket(
            Bucket=bucket_name,
        )
        context = cfntest.get_context()
        create_event = cfntest.get_create_event({
            "Bucket": bucket_name,
            "NotificationConfiguration": {
                "LambdaFunctionConfigurations": [
                    {
                        "Events": ["s3:ObjectCreated:*"],
                        "LambdaFunctionArn": lambda_arn,
                    }
                ]
            }
        })
        update_event = cfntest.get_update_event({
            "Bucket": "test",
            "NotificationConfiguration": {
                "LambdaFunctionConfigurations": [
                    {
                        "Events": ["s3:ObjectCreated:Put"],
                        "LambdaFunctionArn": lambda_arn,
                    }
                ]
            }
        }, cfntest.get_properties(create_event))
        delete_event = cfntest.get_delete_event(cfntest.get_properties(update_event), cfntest.get_properties(create_event))

        if True:
            c = S3BucketNotificationConfiguration(create_event, context)
            c.run()
            self.assertEqual(get_bucket_notification_configuration(bucket_name)['LambdaFunctionConfigurations'][0]['Events'][0], 's3:ObjectCreated:*')

        if True:
            c = S3BucketNotificationConfiguration(update_event, context)
            c.run()
            self.assertEqual(get_bucket_notification_configuration(bucket_name)['LambdaFunctionConfigurations'][0]['Events'][0], 's3:ObjectCreated:Put')

        if True:
            c = S3BucketNotificationConfiguration(delete_event, context)
            c.run()
            self.assertEqual(get_bucket_notification_configuration(bucket_name).get('LambdaFunctionConfigurations'), None)

