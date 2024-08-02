import string 
import random
import numpy as np
from PIL import Image 
from typing import Union
import io
import boto3


def upload_image_to_s3(s3_client: boto3.client,
                       image: Union[str, np.array, Image.Image],
                       s3_bucket: str,
                       s3_key: str
                       ):
    """
    Upload image to S3
    
    Args:
        - image_path (str): Image path
        - s3_bucket (str): S3 bucket name
        - s3_key (str): S3 key
    """
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image).convert("RGB")
    elif isinstance(image, str):
        image = Image.open(image).convert("RGB")
    elif isinstance(image, Image.Image):
        image = image.convert("RGB")


    # 이미지를 BytesIO로 변환
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # S3에 업로드
    s3_client.upload_fileobj(buffer,    
                             s3_bucket,
                             s3_key
                             )
    
    print(f"Image uploaded to S3: {s3_bucket}/{s3_key}")
    

def generate_random_string(max_length=10):
    # 사용할 문자들: 알파벳 대소문자 + 숫자
    characters = string.ascii_letters + string.digits
    
    # 랜덤 문자열 길이: 5에서 max_length까지
    length = random.randint(5, max_length)
    
    # 랜덤 문자열 생성
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string