#!/usr/bin/env python
from operator import itemgetter, or_
import os
import time
import random
import ldclient
from ldclient.config import Config
from dotenv import load_dotenv
from datadog_lambda.metric import lambda_metric

load_dotenv()  # take environment variables from .env.

# Set sdk_key to your LaunchDarkly SDK key before running
sdk_key = os.getenv('SDK_KEY') or ''

# Set feature_flag_key to the feature flag key you want to evaluate
feature_flag_key = os.getenv('FLAG_KEY') or ''


launch_darkly_client = None


def show_message(s):
    print("*** %s" % s)
    print()


def handler(event, context):
    # print(event)

    global launch_darkly_client

    if launch_darkly_client is None:
        if not sdk_key:
            show_message(
                "Please edit test.py to set sdk_key to your LaunchDarkly SDK key first")
            exit()

        ldclient.set_config(Config(sdk_key))

        launch_darkly_client = ldclient.get()

    total_success = 0
    total_failure = 0

    error_rate_max, error_rate_min, error_rate_bump, success_rate_max, success_rate_min, wait_time, iterations = itemgetter('errorRateMax', 'errorRateMin', 'errorRateBump',
                                                                                                                            'successRateMax', 'successRateMin', 'waitSeconds', 'iterations')(event)
    error_rate_max = error_rate_max or 3
    error_rate_min = error_rate_min or 1
    error_rate_bump = error_rate_bump or 3
    success_rate_max = success_rate_max or 15
    success_rate_min = success_rate_min or 10
    iterations = iterations+1 or 1

    # The SDK starts up the first time ldclient.get() is called
    if launch_darkly_client.is_initialized():
        show_message("SDK successfully initialized!")

        # Set up the user properties. This user should appear on your LaunchDarkly users dashboard
        # soon after you run the demo.
        user = {
            "key": "munnawar-unique-user-key",
            "name": "Munnawar"
        }

        flag_value = launch_darkly_client.variation(
            feature_flag_key, user, 'default message')

        good = random.randint(success_rate_min, success_rate_max)

        if flag_value:  # if the feature is on
            bad = random.randint(
                error_rate_min + error_rate_bump, error_rate_max + error_rate_bump)
            lambda_metric('success', good)
            lambda_metric('failure', bad)
            # print('reporting good: ' + str(good) + ' bad: ' + str(bad))
            total_success += good
            total_failure += bad
        else:  # if the feature is off
            # send XX value to the lambda metric
            bad = random.randint(error_rate_min, error_rate_max)
            lambda_metric('success', good)
            lambda_metric('failure', bad)
            # print('reporting good: ' + str(good) + ' bad: ' + str(bad))
            total_success += good
            total_failure += bad

    else:
        raise Exception("SDK failed to initialize")

    return iterations
