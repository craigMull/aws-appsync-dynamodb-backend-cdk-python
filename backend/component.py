from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from typing import Any

import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_appsync_alpha as appsync


class Backend(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsAppsyncDynamodbBackendCdkPythonQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # The code that defines your stack goes here
        api = appsync.GraphqlApi(self, "Api",
            name="demo",
#            schema=appsync.SchemaFile.from_asset(path.join(__dirname, "schema.graphql")),
            schema=appsync.SchemaFile.from_asset("./backend/api/schema.graphql"),
            authorization_config=appsync.AuthorizationConfig(
                default_authorization=appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        # Resolver Mapping Template Reference:
        # https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference-dynamodb.html
        demo_dS.create_resolver("QueryGetDemosResolver",
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver("MutationAddDemoResolver",
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
        
        # To enable DynamoDB read consistency with the `MappingTemplate`:
        demo_dS.create_resolver("QueryGetDemosConsistentResolver",
            type_name="Query",
            field_name="getDemosConsistent",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(True),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )