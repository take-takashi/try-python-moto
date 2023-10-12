import json
import unittest
import boto3
from apis import handler
from http import HTTPStatus
from moto import mock_lambda, mock_dynamodb

# テスト対象のテーブル名
TABLE_NAME = "test-table"


def create_event(body):
    return {"body": json.dumps(body), "requestContext": {}}


class TestHandler(unittest.TestCase):
    # テスト実施前の処理
    def setUp(self) -> None:
        pass

    # テスト実行後の処理
    def tearDown(self) -> None:
        pass

    def create_table(self):
        db = boto3.resource("dynamodb", region_name="ap-northeast-1")
        db.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"KeyType": "HASH", "AttributeName": "id"},
                {"KeyType": "RANGE", "AttributeName": "name"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table = db.Table(TABLE_NAME)
        handler.TEST_TABLE = table
        return table

    @mock_dynamodb
    @mock_lambda
    def test_handler(self):
        # テーブル作成
        table = self.create_table()
        # リクエストパラメータ
        name = "moto-test"
        request = {
            "name": name,
        }
        # lambda実行
        response = handler.handler(create_event(request), {})
        body = json.loads(response["body"])
        # HTTPステータスチェック
        assert HTTPStatus.OK == response["statusCode"]
        # レスポンスメッセージチェック
        assert body["message"] == "DB登録完了"
        # DB登録結果確認
        data = table.scan()["Items"]
        assert len(data) == 1
        assert data[0]["name"] == name
