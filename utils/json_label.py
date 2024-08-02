import boto3
from typing import Dict, List
from PIL import Image 
import json

def read_json_label(bucket: str,
                    key: str,
                    s3_client: boto3.client
                    ):
    """
    Read JSON label
    Read JSON label from the given path
    
    Args:
        - bucket (str): S3 bucket name
        - key (str): S3 key
    
    Returns:
        - json_label (Dict): JSON label
    """
    # Read JSON label
    response = s3_client.get_object(Bucket=bucket,
                                    Key=key
                                    )
    label = response["Body"].read().decode("utf-8")

    # Convert JSON label to dictionary
    json_label = json.loads(label)

    return json_label

def create_connect_t_label(image_path: str,
                           classes: List[str],
                           bboxes: List[List[int]]
                           ) -> Dict:
    """
    Connect-T 형식의 라벨을 만드는 함수 
    
    Args:
        - text (str): OCR 결과 라벨 
        - min_x (int): 최소 x 좌표
        - min_y (int): 최소 y 좌표
        - max_x (int): 최대 x 좌표
        - max_y (int): 최대 y 좌표
    
    Returns:
        - label (Dict): Connect-T 형식의 라벨
    """

    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Create label
    json_label = {
        "api": "1.1",
        "billed_pages": 1,
        "elements": [],
        "metadata": {
            "pages": [
                {
                    "height": width,
                    "width": height,
                    "page": 1
                }
            ]
        }
    }

    # Create element
    for i, (class_, bbox) in enumerate(zip(classes, bboxes)):
        single_element = {
            "text": class_,
            "id": i,
            "html": "null",
            "page": 1,
            "category": "paragraph",
            "bounding_box": [
                {
                    "x": bbox[0],
                    "y": bbox[1]
                },
                {
                    "x": bbox[2],
                    "y": bbox[1]
                },
                {
                    "x": bbox[2],
                    "y": bbox[3]
                },
                {
                    "x": bbox[0],
                    "y": bbox[3]
                }
            ],
            "children": []
        }
        
        # Append element
        json_label["elements"].append(single_element)

    return json_label
