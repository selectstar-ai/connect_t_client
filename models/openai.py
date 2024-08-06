from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import Any, Mapping, Optional
from utils.preprocessing import remove_comments_from_lines

class CustomGpt:
    """LangChain LLM"""

    def __init__(
        self,
        model_name: Optional[str] = "gpt-4o-mini-2024-07-18",
        temperature: Optional[float] = 0.5,
        verbose=False,
    ):
        """
        LangChain LLM 초기 세팅

        Args:
            model_name (Optional[str]): OpenAI API 모델 이름
            instruction (Optional[str]): 모델에 넣어줄 지시문
            seed_prompt (Optional[str]): 고정으로 넣어줄 프롬프트
            temperature (Optional[float]): 재현성을 위해 낮은 값으로 반환한다.
            verbose (bool): debugging을 위해 중간 과정을 출력한다.
        """
        self.verbose = verbose
        self.temperature = temperature
        self.text = ""

        # model: environment에 설정
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)  

    def invoke(
            self, 
            system_prompt: str,
            user_prompt: str,
        ) -> str:

        self.system_message = system_prompt
        self.history_memory = [SystemMessage(content=self.system_message)]
        self.initial_history_memory = [SystemMessage(content=self.system_message)]
        self.user_prompt = user_prompt

        response = self.llm.invoke(
            self.history_memory 
            + [HumanMessage(content=self.user_prompt)]
        )
            
        response = response.content
        response = response.strip()

        self.history_memory.append(HumanMessage(content=self.user_prompt))
        self.history_memory.append(AIMessage(content=response))

        if self.verbose:
            print(self.history_memory)

        return response
    
def llm_response(llm_model: str, system_prompt: str, user_prompt: str, stream: bool = False) -> OpenAI:
    """프롬프트에 대한 LLM의 응답값을 반환한다.

    Args:
        llm_model (str): 사용할 llm model name
        system_prompt: 시스템 프롬프트 (시스템에 역할을 부여하는 역할)
        user_prompt: 유저 프롬프트 (유저의 질의 및 예시를 부여하는 역할)

    Returns:
        completion (OpenAI): 프롬프트에 대한 응답값이 반환되며 openai.types.chat.chat_completion.ChatCompletion 형태
    """

    client = CustomGpt(model_name=llm_model, verbose=stream)
    completion = client.invoke(system_prompt=system_prompt, user_prompt=user_prompt)
    return completion


def make_struct(json_doc:dict) -> dict:
    
    str_json = str(json_doc)
                
    system_prompt = """당신은 주어진 JSON 데이터를 분석하여 주어진 형식을 준수하며 계층적 구조(tree 형식)로 JSON을 재생성하는 전문가이다.
page, category, text를 잘 이해하고 특정 문단의 하위 문단들은 children으로 재배열하여 JSON 구조로 생성하라.
"""
    user_prompt = f"""
다음 JSON들의 text 부분들을 보고 계층화된 tree 형식으로 만들어줘
JSON:
{json_doc}

<<<특징>>>
1. JSON 문법을 준수해서 만들어줘
2. elements 내의 key-value들(boudning_box, category, html, id, text 포함)을 보존해서 만들어줘
3. elements 내에 children이 존재하지 않는 문단이라도 children key를 추가해줘
4. JSON_SCHEMA에 맞춰 결과를 생성해주세요!

<<<문제>>>
- JSON 구조를 잘 해석하여 응답해
- 의미론적인 계층 구조를 만들어서 응답해

<<<JSON_SCHEMA>>> : {{
  "elements": [
      {{
          "bounding_box": [{{
              원래 그대로 복원
          }}],
          "category": 원래 그대로 복원,
          "html": 원래 그대로 복원,
          "id": 원래 그대로 복원,
          "page": 원래 그대로 복원,
          "text": 원래 그대로 복원,
          "children": [
              None or {{"bounding_box","category","html","id","page","text"}}
          ]
      }}
  ]
}}"""
    retry_num = 5   # 재시도 횟수 (limit)
    response_k = 0  # response 재시도 횟수 (기록용)
    k = 0
    while retry_num > 0:
        if response_k >= 10:
            break
        
        response = llm_response("gpt-4o-mini-2024-07-18", f"{system_prompt}", f"{user_prompt}")
        try:
            # 정규표현식을 이용하여 첫 번째 {와 마지막 } 사이의 내용 추출 (DOTALL 플래그 사용)
            match = re.search(r'(\{.*\})', response, re.DOTALL)
        except Exception as e:
            print(f"{j + 1}page 재시도 {response_k+1}", e)
            response_k += 1
            continue
        result = match.group(1)
        result = remove_comments_from_lines(result)
        
        try:
            dict_result = eval(result)
            return dict_result
        
        except Exception as e:
            print(f"재시도 {k+1}", e)
            retry_num -= 1
            k += 1
            continue
    return dict_result