from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from memory.mongo_memory import MongoChatMemory
from backend.tools.post_tool import PostGeneratorTool
from db.posts import save_post, list_user_posts, schedule_post
from langchain.agents.agent_types import AgentType

class PostManagementAgent:
    def __init__(self, user_id, openai_api_key):
        self.user_id = user_id
        self.memory = MongoChatMemory(session_id=user_id)
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)

        self.post_tool = PostGeneratorTool(openai_api_key=openai_api_key)

        tools = [
            Tool(
                name="Post Generator",
                func=self.post_tool._run,
                description="Generate social media posts given a topic and tone"
            ),
            Tool(
                name="Save Post",
                func=self._save_post,
                description="Save a generated post draft with content, platform, and hashtags"
            ),
            Tool(
                name="List Posts",
                func=self._list_posts,
                description="List saved posts with optional status filter"
            ),
            Tool(
                name="Schedule Post",
                func=self._schedule_post,
                description="Schedule a post by post ID and datetime string (ISO format)"
            )
        ]

        self.agent = initialize_agent(tools, self.llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=self.memory)

    def _save_post(self, args_str: str) -> str:
        # args_str example: "content=Hello world; platform=Instagram; hashtags=#fun,#ai"
        args = dict(item.split('=') for item in args_str.split(';'))
        content = args.get("content")
        platform = args.get("platform", "Instagram")
        hashtags = args.get("hashtags", "")
        hashtags_list = [tag.strip() for tag in hashtags.split(',')] if hashtags else []

        post_id = save_post(self.user_id, content, platform, hashtags_list, status="draft")
        return f"Post saved with ID: {post_id}"

    def _list_posts(self, status: str = None) -> str:
        posts = list_user_posts(self.user_id, status)
        if not posts:
            return "No posts found."
        return "\n".join([f"{p['_id']}: {p['content'][:40]}... (status: {p['status']})" for p in posts])

    def _schedule_post(self, args_str: str) -> str:
        # args_str example: "post_id=xyz; scheduled_for=2025-06-10T10:00:00"
        args = dict(item.split('=') for item in args_str.split(';'))
        post_id = args.get("post_id")
        scheduled_for = args.get("scheduled_for")
        if not post_id or not scheduled_for:
            return "post_id and scheduled_for are required."
        success = schedule_post(post_id, scheduled_for)
        return "Post scheduled successfully." if success else "Failed to schedule post."

    def run(self, input_text: str) -> str:
        response = self.agent.run(input_text)
        return response
