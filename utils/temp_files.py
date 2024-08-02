from pathlib import Path 

def check_tmp_file(image_path: str,
                   tmp_dir: str = "tmp/"
                   ) -> bool:
    """
    이미지 경로가 tmp에 저장되어 있는지 확인하는 함수
    이미지 경로를 입력으로 받아, 해당 이미지가 tmp에 저장되어 있는지 확인하고 결과를 반환
    
    만약, 정식 라벨이 존재하는 경우에도 False를 반환하고 tmp 파일을 삭제 

    Args:
        - image_path (str): 이미지 경로
        - tmp_dir (str): 임시 디렉토리 경로

    Returns:
        - is_tmp (bool): 이미지가 tmp에 저장되어 있는지 여부
    """

    # 정식 라벨 존재 여부 확인 
    json_path = Path(image_path).with_suffix(".json")
    temp_image_path = Path(tmp_dir) / Path(image_path).name
    temp_json_path = temp_image_path.with_suffix(".json")
    
    if json_path.exists():  # 정식 라벨이 존재하는 경우, tmp 파일 삭제 후 False 반환
        if temp_image_path.exists():    # 정식 라벨이 존재하고, tmp 파일도 있는 경우
            temp_image_path.unlink()
            temp_json_path.unlink()
        return False

    elif not json_path.exists() and temp_json_path.exists():  # 정식 라벨이 없고, tmp 파일이 존재하는 경우 True 반환
        return True
    
    return False # 모두 없는 경우에는 False 반환

def remove_tmp_file(image_path: str,
                    tmp_dir: str
                    ) -> None: 
    """
    이미지 경로에 해당하는 tmp 파일을 삭제하는 함수
    이미지 경로를 입력으로 받아, 해당 이미지에 해당하는 tmp 파일을 삭제
    이미지 및 json 파일을 삭제
    
    Args:
        - image_path (str): 이미지 경로
        - tmp_dir (str): 임시 dir
    """
    temp_path = Path(tmp_dir) / Path(image_path).name
    json_path = Path(tmp_dir) / Path(image_path).with_suffix(".json").name

    if temp_path.exists():
        temp_path.unlink()
    if json_path.exists():
        json_path.unlink()