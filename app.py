#!/usr/bin/env python3
import os

import aws_cdk as cdk

from backup_s3.backup_s3_stack import BackupS3Stack
# from backup_s3.backup_s3_stack import BackupS3Stack other

app = cdk.App()
BackupS3Stack(app, "CF1234BackupS3Stackdev")
BackupS3Stack1(app, "CF1234BackupS3Stackdev1")
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    # )

app.synth()  # --all