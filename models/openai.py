from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import Any, Mapping, Optional

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