from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    aws_iam as iam,
    aws_ecr_assets as ecr_assets,
    aws_lambda as lambda_,
)
from constructs import Construct

import json


class AwsCdkS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # 1. Create an S3 bucket
        bucket = s3.Bucket(
            self,
            "MyBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 2. Create a DynamoDB table

        # Define the table schema
        partition_key = dynamodb.Attribute(
            name="id", type=dynamodb.AttributeType.STRING
        )
        sort_key = dynamodb.Attribute(
            name="sortKey", type=dynamodb.AttributeType.NUMBER
        )

        # Make table
        table = dynamodb.Table(
            self,
            "MyTable",
            table_name="test-table",
            partition_key=partition_key,
            sort_key=sort_key,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # 3. IAM role for Lambda
        with open("policy.json", "r") as policy_file:
            assume_role_policy_document = json.load(policy_file)

        lambda_role = iam.Role(
            self,
            "LambdaBasicRole",
            role_name="lambda-S3function-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "AssumeRolePolicy": iam.PolicyDocument.from_json(
                    assume_role_policy_document
                )
            },
        )

        # Grant necessary permissions to the role
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        # 4. Create Lambda Function
        lambda_function = lambda_.DockerImageFunction(
            self,
            "MyLambdaFunction",
            function_name="S3-DynamoDB-function",
            code=lambda_.DockerImageCode.from_image_asset(
                "./", platform=ecr_assets.Platform.LINUX_AMD64
            ),
            environment={"BUCKET_NAME": bucket.bucket_name},
            timeout=Duration.seconds(900),
            memory_size=384,
            role=lambda_role,
        )

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsCdkS3Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
