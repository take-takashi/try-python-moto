from aws_lambda_typing import context as context_, events
import http
import typing

class ResponseType(typing.TypedDict):
    statusCode: http.HTTPStatus
    body: 


def lambda_handler(event: events.S3Event, context: context_.Context) -> ResponseType:
    
    return new ResponseType(
        statusCode=http.HTTPStatus.OK,

    )