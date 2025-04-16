from aws_cdk import (
    App, Stack,
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
    aws_lambda as _lambda,
    aws_iam as iam,
    core,
)
from constructs import Construct

class ServerlessCacheStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 从 cdk.json 配置中读取 VPC 和 Subnet 信息
        vpc_id = self.node.try_get_context("vpc_id")
        subnet_ids = self.node.try_get_context("subnet_ids")

        if not vpc_id or not subnet_ids:
            raise ValueError("VPC ID or Subnet IDs not found in cdk.json")

        # 获取 VPC 和 Subnet
        vpc = ec2.Vpc.from_vpc_attributes(self, "VPC", vpc_id=vpc_id, availability_zones=["us-west-2a", "us-west-2b"])

        # 创建一个安全组，根据 Subnet IDs 配置
        security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="ServerlessCacheSG"
        )

        # 限制安全组访问，只允许特定的 IP 地址访问
        security_group.add_ingress_rule(
            ec2.Peer.ipv4("10.0.0.0/24"),
            ec2.Port.tcp(6379),  # 例子：假设你使用的是 Redis 的默认端口
            "Allow access to Redis"
        )

        # 创建 Serverless Lambda 作为缓存（Serverless Cache）
        serverless_cache = _lambda.Function(self, "ServerlessCacheFunction",
            runtime=_lambda.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/"),  # 假设你在 `lambda/` 目录下有 Lambda 代码
            environment={
                "CACHE_TYPE": "Redis"
            },
            vpc=vpc,
            security_groups=[security_group],  # 配置 Lambda 绑定到安全组
            subnet_selection=ec2.SubnetSelection(
                subnet_ids=subnet_ids  # 指定 Subnet IDs
            ),
        )

        # 输出 VPC 和 Subnet 信息
        core.CfnOutput(self, "VPCId", value=vpc.vpc_id)
        core.CfnOutput(self, "SecurityGroupId", value=security_group.security_group_id)

app = App()
ServerlessCacheStack(app, "ServerlessCacheStack")
app.synth()