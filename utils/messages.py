# IO
from typing import Any, Dict, Union, List
import json

# ETC 
import boto3
from time import time

# Custom libraries
from utils.json_label import read_json_label


# TODO SQS URL 채우기 
LOCAL2SERVER_SQS_URL = "https://sqs.ap-northeast-2.amazonaws.com/292286933749/connect_t_local2server"
SERVER2LOCAL_SQS_URL = "https://sqs.ap-northeast-2.amazonaws.com/292286933749/connect_t_server2local"

def produce_message(key: str,
                    task: str
                    ):
    """
    Produce a message to SQS queue
    Send a message to SQS queue with the image array
    The message is base64 encoded image
    
    Args: 
        - task (str): Task to perform
        - key (str): Key to save the image in S3

    Returns:
        - message (str): Message to send
    """
    # Make the message 
    message = {
        "bucket": "ocr-labeler",
        "key": key,
        "task": task,
        "id": key.split(".jpg")[0]
    }

    # Convert message to JSON
    message = json.dumps(message)

    return message 

def send_message(sqs_client: Any, 
                 message: str
                 ):
    """
    Send a message to SQS queue
    Send a message to SQS queue with the message
    
    Args:
        - sqs_client (Any): SQS client
        - message (str): Message to send include id 
    """
    # Send message to SQS queue
    sqs_client.send_message(QueueUrl=LOCAL2SERVER_SQS_URL,
                            MessageBody=message
                            )


def consume_message_ocr(sqs_client: Any,
                        message_id: str
                        ) -> str:
    """
    Consume a message from SQS queue
    Receive a message from SQS queue and decode the message
    For OCR, the message is base64 encoded image
    
    Args:
        - sqs_client (Any): SQS client
        - message_id (str): Message id

    Returns:
        - text (str): OCR result
    """
    start_time = time()

    while True:
        response = sqs_client.receive_message(QueueUrl=SERVER2LOCAL_SQS_URL,
                                              MaxNumberOfMessages=1,
                                              WaitTimeSeconds=2  # Long polling wait time (0~20)
                                              )
        
        if "Messages" in response:
            message = response["Messages"][0]

            # convert str message to dict 
            message_body = json.loads(message["Body"])            
            id: str = message_body["id"]

            if message_id == id:
                text: str = message_body["text"]
                del_handle: str = message["ReceiptHandle"]
                print(f"메시지를 수신하였습니다. {text}")

                # convert \n to <SEP> Token 
                text = text.replace("\n", "<SEP>")
                break
            else:
                print("메시지 ID가 일치하지 않습니다. 다시 수신합니다.")

        else:
            print("수신되는 메시지가 없습니다.")
        
        if time() - start_time > 15:
            text = ""
            del_handle = None
            print("데이터가 오지 않아 프로세스를 종료합니다.")
            break
    
    # delete message
    if del_handle:
        delete_message(sqs_client=sqs_client,
                       handle=del_handle
                       )

    return text


def consume_message_lda(sqs_client: boto3.client,
                        s3_client: boto3.client,
                        message_id: str
                        ):
    """
    Consume a message from SQS queue
    Receive a message from SQS queue and decode the message
    For LDA, the message is base64 encoded image
    
    Args:
        - sqs_client (Any): SQS client
        - s3_client (Any): S3 client
        - message_id (str): Message id

    Returns:
        - classes (List): Detected classes
        - boxes (List): Detected boxes
    """
    classes: List[str] = []
    boxes: List[Dict[str, Union[int, float]]] = []

    start_time = time()

    while True:
        response = sqs_client.receive_message(QueueUrl=SERVER2LOCAL_SQS_URL,
                                              MaxNumberOfMessages=1)
        if "Messages" in response:
            message = response["Messages"]
            handle = message[0]["ReceiptHandle"]

            # Convert message to JSON
            try:
                message = json.loads(message[0]["Body"])
                id: str = message["id"]

                if message_id == id:
                    print(f"메시지를 수신하였습니다. {id} ")
                else: 
                    print("메시지 ID가 일치하지 않습니다. 다시 수신합니다.")
                    continue
            except json.JSONDecodeError:
                print("메시지를 JSON으로 변환할 수 없습니다.")
                continue
            
            bucket = message["bucket"]
            key = message["key"]

            # Read JSON label
            json_label = read_json_label(bucket=bucket,
                                         key=key,
                                         s3_client=s3_client
                                         )
            classes = json_label["classes"]
            boxes = json_label["bboxes"]

            # delete message
            delete_message(sqs_client=sqs_client,
                           handle=handle
                           )
            break
        else:
            print("수신되는 메시지가 없습니다.")
        
        if time() - start_time > 60:
            classes = []
            boxes = []

            print("데이터가 오지 않아 프로세스를 종료합니다.")
            break

    return classes, boxes


def delete_message(sqs_client: boto3.client,
                   handle: str
                   ) -> None:
    """
    Delete a message from SQS queue
    Delete a message from SQS queue with the message handle
    
    Args:
        - sqs_client (Any): SQS client
        - handle (str): Message handle
    """
    sqs_client.delete_message(QueueUrl=SERVER2LOCAL_SQS_URL,
                              ReceiptHandle=handle)
