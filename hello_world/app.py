from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, idempotent, IdempotencyConfig
)
import boto3
import os

idem_config=IdempotencyConfig(event_key_jmespath="body")
jls_extract_var = os.environ['IDEMPOTENT_TABLE']
print ('Idempotency Table Name: ' + jls_extract_var)
persistence_layer = DynamoDBPersistenceLayer(table_name=jls_extract_var)

def test_insert():
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(os.environ['IDEMPOTENT_TABLE'])
    table.put_item (Item={'id':'123456789','record':'blahblah'})


@idempotent(config=idem_config, persistence_store=persistence_layer)
# @idempotent(persistence_store=persistence_layer)
def lambda_handler(event, context):
    # payment = create_subscription_payment(
    #     user=event['user'],
    #     product=event['product_id']
    # )
    # test_insert()

    return {
        "message": "success",
        "statusCode": 200,
    }