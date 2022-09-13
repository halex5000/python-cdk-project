import os
from typing import Mapping
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_alpha,
    aws_stepfunctions as state_machines,
    aws_stepfunctions_tasks as tasks
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

        munnawarPythonFunction = lambda_alpha.PythonFunction(self, "munnawars-function",
                                                             entry="./munnawar_python_function/",  # required
                                                             runtime=lambda_.Runtime.PYTHON_3_8,  # required
                                                             index="index.py",  # optional, defaults to 'index.py'
                                                             handler="handler",
                                                             environment={'SDK_KEY': sdk_key,
                                                                          'FLAG_KEY': feature_flag_key}
                                                             )

        datadog.add_lambda_functions([munnawarPythonFunction])

        make_stats = tasks.LambdaInvoke(self, "Make Stats",
                                        lambda_function=munnawarPythonFunction,  # type: ignore
                                        result_path="$.iterations",
                                        payload_response_only=True,
                                        # payload=state_machines.TaskInput.from_object({
                                        #     "$.errorRateMax": state_machines.JsonPath.number_at("$.errorRateMax"),
                                        #     "$.errorRateMin": state_machines.JsonPath.number_at("$.errorRateMin"),
                                        #     "$.errorRateBump": state_machines.JsonPath.number_at("$.errorRateBump"),
                                        #     "$.successRateMax": state_machines.JsonPath.number_at("$.successRateMax"),
                                        #     "$.successRateMin": state_machines.JsonPath.number_at("$.successRateMin"),
                                        #     "$.waitSeconds": state_machines.JsonPath.number_at("$.waitSeconds"),
                                        #     "$.iterations": state_machines.JsonPath.number_at("$.iterations")
                                        # })
                                        )

        job_success = state_machines.Succeed(self, "Success")

        wait_x = state_machines.Wait(self, "Wait X Seconds",
                                     time=state_machines.WaitTime.seconds_path(
                                         "$.waitSeconds")
                                     ).next(make_stats)

        yo_we_finished_yet = state_machines.Choice(self, 'check if we have done too many iterations').when(
            state_machines.Condition.number_greater_than_equals("$.iterations", 1000), job_success).otherwise(wait_x)

        definition = make_stats.next(yo_we_finished_yet)

        # Create state machine
        sm = state_machines.StateMachine(
            self, "munnawar-datadog-statemachine",
            definition=definition,
            timeout=Duration.minutes(30),
        )
