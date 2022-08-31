from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_alpha
)
from constructs import Construct


class PythonCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "PythonCdkProjectQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        lambda_alpha.PythonFunction(self, "munnawars-function",
                                    entry="./",  # required
                                    runtime=lambda_.Runtime.PYTHON_3_8,  # required
                                    index="munnawar_python_function.py",  # optional, defaults to 'index.py'
                                    handler="show_message"
                                    )
