#!/usr/bin/env python
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

wait = 2
error_rate_max = 3
error_rate_min = 1
error_rate_bump = 3
success_rate_max = 15
success_rate_min = 10
iterations = 10


def show_message(s):
    print("*** %s" % s)
    print()


def handler(event, context):
    if not sdk_key:
        show_message(
            "Please edit test.py to set sdk_key to your LaunchDarkly SDK key first")
        exit()

    ldclient.set_config(Config(sdk_key))

    total_success = 0
    total_failure = 0
    # The SDK starts up the first time ldclient.get() is called
    if ldclient.get().is_initialized():
        show_message("SDK successfully initialized!")

        for x in range(iterations):
            # Set up the user properties. This user should appear on your LaunchDarkly users dashboard
            # soon after you run the demo.
            user = {
                "key": "munnawar-unique-user-key",
                "name": "Munnawar"
            }

            flag_value = ldclient.get().variation(feature_flag_key, user, 'default message')

            # show_message("Feature flag '%s' is %s for this user" %
            #              (feature_flag_key, flag_value))

            # increment the 200 status code (the good)
            # no matter the flag state

            good = random.randint(success_rate_min, success_rate_max)

            # if flag status is GOOD
            if (flag_value == 'Buongiorno'):
                # send XX value to the lambda metric
                bad = random.randint(error_rate_min, error_rate_max)
                lambda_metric('success', good)
                lambda_metric('failure', bad)
                print('reporting good: ' + str(good) + ' bad: ' + str(bad))
                total_success += good
                total_failure += bad
            # continue the while
            else:
                bad = random.randint(
                    error_rate_min + error_rate_bump, error_rate_max + error_rate_bump)
                lambda_metric('success', good)
                lambda_metric('failure', bad)
                print('reporting good: ' + str(good) + ' bad: ' + str(bad))
                total_success += good
                total_failure += bad

            # sleep a little
            time.sleep(wait)

            # if the flag_state is ON
            # break the while loop and enter a new while loop where it increments
            # bad things

    else:
        raise Exception("SDK failed to initialize")

    # Here we ensure that the SDK shuts down cleanly and has a chance to deliver analytics
    # events to LaunchDarkly before the program exits. If analytics events are not delivered,
    # the user properties and flag usage statistics will not appear on your dashboard. In a
    # normal long-running application, the SDK would continue running and events would be
    # delivered automatically in the background.
    # ldclient.get().close()

    return {
        'total_success': total_success,
        'total_failure': total_failure
    }
