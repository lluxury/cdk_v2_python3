from aws_cdk import (
    App, Stack,
    aws_iam as iam,
    core
)
from constructs import Construct

class IamRoleStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 创建 IAM 角色
        iam_role = iam.Role(self, "MyIAMRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),  # 假设角色用于 EC2
            description="IAM Role for EC2 with S3 Access"
        )

        # 为角色添加 S3 权限策略
        iam_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:*"],  # 给与 S3 所有操作权限，按需修改
            resources=["arn:aws:s3:::*"],  # 默认给所有 S3 存储桶权限
            effect=iam.Effect.ALLOW
        ))

        # 输出角色 ARN
        core.CfnOutput(self, "IamRoleArn",
            value=iam_role.role_arn,
            description="IAM Role ARN"
        )

app = App()
IamRoleStack(app, "IamRoleStack")
app.synth()
