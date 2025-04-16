from aws_cdk import (
    App, Stack,
    aws_iam as iam,
    core
)
from constructs import Construct

class WebIdentityFederatedIamRoleStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 创建 IAM 角色，允许通过 Web 身份验证假设角色
        federated_role = iam.Role(self, "FederatedWebIdentityRole",
            assumed_by=iam.FederatedPrincipal(
                federated_provider="arn:aws:iam::aws:policy/AmazonCognitoPowerUser",  # 外部身份提供者的 ARN
                # 使用 Web 身份验证机制
                assume_role_action="sts:AssumeRoleWithWebIdentity",
                conditions={
                    "StringEquals": {
                        "aws:RequestTag/Environment": "Production"  # 额外的条件：请求标签为生产环境
                    }
                }
            ),
            description="A role that can be assumed by federated users using Web Identity"
        )

        # 为角色添加访问某 S3 存储桶的权限
        federated_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:PutObject"],  # 允许访问 S3 存储桶的对象
            resources=["arn:aws:s3:::my-bucket/*"],  # 指定存储桶资源
            effect=iam.Effect.ALLOW,
            conditions={
                "IpAddress": {
                    "aws:SourceIp": "192.168.1.0/24"  # 限制只能从特定 IP 地址范围访问
                }
            }
        ))

        # 输出角色 ARN
        core.CfnOutput(self, "FederatedWebIdentityRoleArn",
            value=federated_role.role_arn,
            description="The ARN of the federated role assumed by Web Identity"
        )

app = App()
WebIdentityFederatedIamRoleStack(app, "WebIdentityFederatedIamRoleStack")
app.synth()





# from aws_cdk import (
#     App, Stack,
#     aws_iam as iam,
#     core
# )
# from constructs import Construct

# class IamRoleStack(Stack):
#     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)

#         # 创建 IAM 角色
#         iam_role = iam.Role(self, "MyIAMRole",
#             assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),  # 假设角色用于 EC2
#             description="IAM Role for EC2 with S3 Access"
#         )

#         # 为角色添加 S3 权限策略
#         iam_role.add_to_policy(iam.PolicyStatement(
#             actions=["s3:*"],  # 给与 S3 所有操作权限，按需修改
#             resources=["arn:aws:s3:::*"],  # 默认给所有 S3 存储桶权限
#             effect=iam.Effect.ALLOW
#         ))

#         # 输出角色 ARN
#         core.CfnOutput(self, "IamRoleArn",
#             value=iam_role.role_arn,
#             description="IAM Role ARN"
#         )

# app = App()
# IamRoleStack(app, "IamRoleStack")
# app.synth()
