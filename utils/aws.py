import boto3
import os 
import yaml 

# Load AWS credentials from yaml file 
with open("config.yaml", "r") as f:
    credentials = yaml.safe_load(f)

AWS_ACCESS_KEY_ID = credentials["AWS"]["ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = credentials["AWS"]["SECRET_KEY"]

def sqs_init():
    """
    Initialize SQS client
    
    Returns:
        - sqs_client (boto3.client): SQS client     
    """
    # TODO - Access Key ID, Secret Access Key 채우기
    sqs_client = boto3.client('sqs',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name="ap-northeast-2")
    
    return sqs_client

def s3_init():
    """
    Initialize S3 client
    
    Returns:
        - s3_client (boto3.client): S3 client     
    """
    # TODO - Access Key ID, Secret Access Key 채우기
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             region_name="ap-northeast-2")
    
    return s3_client
                              
