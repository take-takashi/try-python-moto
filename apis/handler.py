import boto3
import json
import uuid
from aws_lambda_typing import context as context_, events
from typing import TypedDict
from http import HTTPStatus


class BodyType(TypedDict):
    name: str


DYNAMO_DB = boto3.resource("dynamodb", region_name="ap-northeast-1")
TEST_TABLE = DYNAMO_DB.Table("test-table")


def handler(event, context: context_.Context):
    # リクエストパラメータ取得
    body: BodyType = json.loads(event.get("body") or "{}")
    # TODO ref: https://d-oshige.blogspot.com/2021/11/python-moto-unittest.html
    item = {"id": str(uuid.uuid4()), "name": body.get("name")}

    TEST_TABLE.put_item(Item=item)

    return {"statusCode": HTTPStatus.OK, "body": json.dumps({"message": "DB登録完了"})}
