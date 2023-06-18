import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_appsync_dynamodb_backend_cdk_python.aws_appsync_dynamodb_backend_cdk_python_stack import AwsAppsyncDynamodbBackendCdkPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_appsync_dynamodb_backend_cdk_python/aws_appsync_dynamodb_backend_cdk_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsAppsyncDynamodbBackendCdkPythonStack(app, "aws-appsync-dynamodb-backend-cdk-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
