from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import PrivateAttr

class PostGeneratorTool(BaseTool):
    name:str = "post_generator"
    description:str = "Generates social media posts based on a topic and tone."
    _llm: ChatOpenAI = PrivateAttr()
    _prompt_template: PromptTemplate = PrivateAttr()

    def __init__(self, openai_api_key: str, **kwargs):
        super().__init__(**kwargs)
        self._llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)
        self._prompt_template = PromptTemplate(
            input_variables=["topic", "tone"],
            template="Write a {tone} social media post post about {topic}."
        )

    def _run(self, topic: str, tone: str = "friendly") -> str:
        prompt = self._prompt_template.format(topic=topic, tone=tone)
        response = self._llm(prompt)
        return response.content

    async def _arun(self, topic: str, tone: str = "friendly") -> str:
        raise NotImplementedError("Async not implemented")
