import os
from typing import Mapping
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_alpha
)
from constructs import Construct
from dotenv import load_dotenv
from datadog_cdk_constructs_v2 import Datadog


load_dotenv()  # take environment variables from .env.

# Set sdk_key to your LaunchDarkly SDK key before running
sdk_key = os.getenv('SDK_KEY') or ''

# Set feature_flag_key to the feature flag key you want to evaluate
feature_flag_key = os.getenv('FLAG_KEY') or ''

datadog_site = os.getenv('DATADOG_SITE') or ''
datadog_api_key = os.getenv('DATADOG_API_KEY') or ''


class PythonCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        datadog = Datadog(self, "munnawars-function-datadog",
                          python_layer_version=62,
                          extension_layer_version=28,
                          site=datadog_site,
                          api_key=datadog_api_key,
                          )

        # example resource
        # queue = sqs.Queue(
        #     self, "PythonCdkProjectQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        munnawarPythonFunction = lambda_alpha.PythonFunction(self, "munnawars-function",
                                                             entry="./munnawar_python_function/",  # required
                                                             runtime=lambda_.Runtime.PYTHON_3_8,  # required
                                                             index="index.py",  # optional, defaults to 'index.py'
                                                             handler="handler",
                                                             timeout=Duration.seconds(
                                                                 60),
                                                             environment={'SDK_KEY': sdk_key,
                                                                          'FLAG_KEY': feature_flag_key}
                                                             )

        datadog.add_lambda_functions([munnawarPythonFunction])
