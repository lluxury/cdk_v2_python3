from aws_cdk import aws_iam, aws_backup, Stack, Tags
from aws_cdk import aws_secretsmanager as secretsmanager
# from aws_cdk import aws_ecr_assets as ecr_assets
from constructs import Construct




class SecretManagementStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        secret = secretsmanager.Secret(self, "MySecret",
            secret_name="MySecretName",  # 可选，指定机密的名称
            description="This is a secret for my application",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"myuser"}',  # 初始的 Secret JSON 模板
                generate_string_key="password",  # 生成的密钥名称
                exclude_punctuation=True,  # 不包含标点符号
                password_length=16  # 密码长度
            )
        )

        # 为 Secret 打标签
        core.Tags.of(secret).add("Environment", "Production")
        core.Tags.of(secret).add("Application", "MyApp")

        # # 为 EC2 Role 授予访问 Secret 的权限
        # role = iam.Role(self, "EC2SecretAccessRole",
        #     assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        # )
        
        # # 给角色添加 Secrets Manager 访问权限
        # role.add_to_policy(iam.PolicyStatement(
        #     actions=["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
        #     resources=[secret.secret_arn]  # 只允许访问该 Secret
        # ))

        # # 打标签到角色
        # core.Tags.of(role).add("Role", "EC2SecretAccessRole")

        # # 输出 Secrets Manager 机密的 ARN
        # self.secret_arn = secret.secret_arn

        # print(f"Secret ARN: {self.secret_arn}")