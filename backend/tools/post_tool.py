from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class PostGeneratorTool(BaseTool):
    name = "post_generator"
    description = "Generates social media posts based on a topic and tone."

    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)
        self.prompt_template = PromptTemplate(
            input_variables=["topic", "tone"],
            template="Write a {tone} social media post post about {topic}."
        )

    def _run(self, topic: str, tone: str = "friendly") -> str:
        prompt = self.prompt_template.format(topic=topic, tone=tone)
        response = self.llm(prompt)
        return response.content

    async def _arun(self, topic: str, tone: str = "friendly") -> str:
        raise NotImplementedError("Async not implemented")
