# cdk_v2_python3

mkdir MyEcsConstruct
cd MyEcsConstruct
cdk init --language python
source .venv/bin/activate # On Windows, run '.\venv\Scripts\activate' instead
pip install -r requirements.txt

export AWS_ACCESS_KEY_ID

cdk bootstrap --profile yann aws://2345/us-east-1


cdk synth
cdk deploy --all


使用多个cdk.json 区分环境，一个项目一个代码库或目录
app 负责调度，子目录为环境
