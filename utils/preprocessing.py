import unicodedata

def normalize_to_nfc(s: str) -> str:
        """
        문자열을 NFC 형식으로 정규화합니다.
        Args:
            s (str): 변환할 문자열
        Returns:
            str: NFC 형식으로 변환된 문자열
        """
        return unicodedata.normalize("NFC", s)
    
def remove_comments_from_lines(text):
    # 입력 문자열을 줄 단위로 분리합니다.
    lines = text.splitlines()
    
    # 각 줄에서 "//" 이후의 내용을 제거합니다.
    cleaned_lines = [line.split('//')[0].rstrip() for line in lines]
    
    # 처리된 줄들을 다시 하나의 문자열로 조합합니다.
    return "\n".join(cleaned_lines)