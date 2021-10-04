## Library for Idempotent operations 

**Idempotent operations** will return the same result on successful
completion, when they are called multiple times with the same
parameters. This makes idempotent operations **safe to retry**.

In mathematical terms f(x) = f(f(x)) and so on.

This feature is important in the case of Integration Software, because
the same message may arrive twice. An example where this could happen in
a PRIDE example is given below:

Say, the PRIDE tier gets a Pre-Fund request from ACH+. PRIDE processes the
message and interacts with FiServ DNA. But before sending the response
back, there was an interruption in the AWS Availability Zone, and
ACHplus did not get a response back. Now, we don’t know what the retry
logic of ACH+ is. They may resend that message to PRIDE within a few
seconds. PRIDE has two choices, send the second Hold request also to
DNA (one of them will eventually age out), OR not sending the second
request to DNA, but send the same response back to ACH+ as the first
request. If the PRIDE service does the second way, the service is
considered idempotent. This can be achieved by PRIDE by adding a certain
logic, which says that if it gets the exact same request-payload within
a certain time, the second could be considered a duplicate, and send
back the results of the first, which is stored in our temporary storage.

Another example where idempotent functionality is important is when
a function is being invoked from another AWS Asynchronous service
that has an execution semantic of “at least once”; For example, SQS or
Express Workflows in Step Functions. If the lambda function is getting
called through one of these, then the Lambda needs to ensure that the
results of the first invocation are stored, and the same result is
returned for each subsequent invocation.

This document doesn’t recommend which PRIDE services need to be idempotent or
not, as that is a business decision. This document specifically
discusses the coding aspects to be incorporated, if a service is deemed
to be coded as idempotent.

## Suggested Solution

[<u>PowerTools for
Python</u>](https://awslabs.github.io/aws-lambda-powertools-python/develop/utilities/idempotency/)
is the suggested tool for ensuring Idempotency. Other than meeting the
basic requirements above, it has the following features:

-   Select a subset of the request as the idempotency key using JMESPath
    > expressions

-   Set a time window in which records with the same payload should be
    > considered duplicates


## How to deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Use the SAM CLI to build and deploy`

Build your application with the `sam build --use-container` command.

```bash
ptools4lam-idem$ sam build --use-container
```

Deploy to aws using `sam deploy --guided` command.

```bash
ptools4lam-idem$ sam deploy --guided
```