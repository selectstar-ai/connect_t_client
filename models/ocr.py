import numpy as np

# ETC 
import boto3
import time 

# Custom Libraries
from utils.messages import produce_message, send_message, consume_message_ocr
from utils.image_handling import upload_image_to_s3, generate_random_string

def pororo_ocr(img_patch: np.array,
               sqs_client: boto3.client,
               s3_client: boto3.client,
               latex_mode: bool = False
               ) -> str:

    message: str
    key: str

    # Generate random string for key 
    key = generate_random_string() + ".jpg"

    # Produce message to SQS
    if latex_mode:
        task = "latex_ocr"
    else: 
        task = "ocr"
    message = produce_message(key=key,
                              task=task,
                              )
    
    # Save image to S3
    upload_image_to_s3(s3_client=s3_client,
                       image=img_patch,
                       s3_bucket="ocr-labeler",
                       s3_key=key
                       )

    # Send message to SQS queue
    send_message(sqs_client=sqs_client,
                 message=message
                 )
    
    print(f"메시지를 발송하였습니다. key: {key}")

    # Get response from Pororo OCR API 
    text: str = consume_message_ocr(sqs_client=sqs_client,
                                    message_id=key.split(".jpg")[0]
                                    )

    return text