# Python CDK Starter



## prerequisites:
1. NPM 6+ installed
2. AWS CDK command line installed: `npm install -g aws-cdk`
3. AWS CLI installed and configured: https://aws.amazon.com/cli/ 
4. Docker CLI installed:  https://docs.rancherdesktop.io/getting-started/installation 
(recommend installing rancher instead as it is free, but Docker itself requires a license now, this install includes the Docker CLI without license constraints)

## to use this as is and deploy to your account, do the following:

1. make a copy of `.env.example`
2. rename to `.env`
3. Update `.env` with your SDK key and Flag key
4. Run 
    ```shell
    python3 -m venv .venv
    ```
5. Run 
    ```shell
    source .venv/bin/activate
    ```
6. Run 
    ```shell
    pip install -r requirements.txt
    ```
7. cd to the `munnawar_python_function` directory
8. Run 
    ```shell
    pip install -r requirements.txt
    ``` 
again (the function has different dependencies than the project)
9. to run the function locally, run 
    ```shell
    ./index.py
    ``` 
in the terminal, if this doesn't work, run 
    ```
    chmod u+x ./index.py
    ```
should change perms to allow execute
10.  to deploy run 
    ```
    cdk deploy
    ``` 
from within the project root. this will use environment variables from 


## Handy links for AWS CDK & LaunchDarkly using Python:
- getting started with the CDK: https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html
- python CDK example: https://github.com/aws-samples/aws-cdk-examples/tree/master/python/dynamodb-lambda
- python CDK docs: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/README.html
- LaunchDarkly python SDK docs: https://docs.launchdarkly.com/sdk/server-side/python
- Sample LaunchDarkly python app: https://github.com/launchdarkly/hello-python
- AWS Lambda CDK Python Docs: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
- Experimental CDK Python Lambda Function construct docs: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda_python_alpha/README.html
  

## Boilerplate CDK README below:


-----

## Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
