# Connect T 추론용 Client 


<br>

## 사용 방법 

1. **Config 파일 수정**    
    1-1. `config.yaml` 파일을 열어줍니다.    
    1-2. config 파일의 `img_path` 키에 추론하고자 하는 문서(이미지)의 경로를 입력해줍니다.    
    1-3. 수식을 추론하는 경우, `latex_mode`를 True로 변경해줍니다. 

<br>

2. **환경 설치** 

```bash 
pip install -r requirements.txt
```

<br>

3. **추론 진행** 

```bash 
python main.py
```
