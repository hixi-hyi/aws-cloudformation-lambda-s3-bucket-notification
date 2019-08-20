# cfn-lambda-s3-bucket-notification-configuration
## Description
The `cfn-lambda-s3-bucket-notification-configuration` function is CloudFormation Custom Lambda that support of create `s3 bucket notification configuration`

See also official documentation.
* https://aws.amazon.com/premiumsupport/knowledge-center/unable-validate-circular-dependency-cloudformation/?nc1=h_ls

## When do you use it
* Declare notifications independently of `AWS::S3::Bucket`

## Caution
The function replace all notifications if you created it.
You must be created notifications with this resource(function) only.

## Deploy
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#deploy)

## Usage
```
  S3Bucket:
    Type: AWS::S3::Bucket
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref S3Bucket
      PolicyDocument:
        Statement:
          - Action:
              - "s3:PutBucketNotification"
            Effect: "Allow"
            Resource: !GetAtt S3Bucket.Arn
            Principal:
              AWS: !ImportValue cfn-lambda-s3-bucket-notification-configuration:LambdaRoleArn
  S3BucketNofiticationConfiguration:
    Type: Custom::Lambda
    DependsOn: S3BucketPolicy
    Properties:
      ServiceToken: !ImportValue cfn-lambda-s3-bucket-notification-configuration:LambdaArn
      Bucket: !Ref S3Bucket
      NotificationConfiguration:
        LambdaFunctionConfigurations:
          - Events:
              - s3:ObjectCreated:*
            LambdaFunctionArn: !GetAtt LambdaFunction.Arn
      DeployAlways: !Ref Date
      Policies:
        Deletion:
          - IgnoreError
```

## Parameters
The function implements [s3api put-bucket-notification-configuration](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-notification-configuration.html)

### Bucket
- BucketName
- ***Required:*** Yes
- ***Update requires:*** Replacement

### NotificationConfiguration
- [Docs](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification)
- ***Required:*** Yes
- ***Update requires:*** No interruption


### Policies.Deletion (optional)
- Support values are `IgnoreError` and `Retain`.
  - `IgnoreError`
- ***Required:*** No
- ***Update requires:*** No interruption


## Contributing
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#contributing)
