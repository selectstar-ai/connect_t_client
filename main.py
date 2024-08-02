from models.ocr import pororo_ocr
from utils.aws import sqs_init, s3_init
import yaml 
import numpy as np 
from PIL import Image 

# Load config file 
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

is_latex_mode = config["latex_mode"]

# Load image
img_path = config['img_path']
img = Image.open(img_path).convert('RGB')
img = np.array(img)

# AWS clients init 
sqs_client = sqs_init()
s3_client = s3_init()


# Inference 
text = pororo_ocr(img_patch=img,
                  sqs_client=sqs_client,
                  s3_client=s3_client,
                  latex_mode=is_latex_mode
                  )

print(text)