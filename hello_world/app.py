from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, idempotent, IdempotencyConfig
)
# import boto3
import os
import requests
import random


idem_config = IdempotencyConfig(event_key_jmespath="body")
print('Idempotency Table Name: ' + (os.environ['IDEMPOTENT_TABLE']))
persistence_layer = DynamoDBPersistenceLayer(
    table_name=os.environ['IDEMPOTENT_TABLE'])


def test_func():
    # ddb = boto3.resource('dynamodb')
    # table = ddb.Table(os.environ['IDEMPOTENT_TABLE'])
    # table.put_item (Item={'id':'123456789','record':'blahblah'})
    ret_var = (requests.
               get('https://jsonplaceholder.typicode.com/users/{}'.
                   format(random.randint(1, 10)))).json()['name']
    print(ret_var)
    return (ret_var)


@idempotent(config=idem_config, persistence_store=persistence_layer)
# @idempotent(persistence_store=persistence_layer)
def lambda_handler(event, context):
    # payment = create_subscription_payment(
    #     user=event['user'],
    #     product=event['product_id']
    # )
    # test_insert()
    response = test_func()

    return {
        "message": response,
        "statusCode": 200,
    }
