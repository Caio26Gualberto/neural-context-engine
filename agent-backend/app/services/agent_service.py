import json

from openai import OpenAI

from app.tools.registry import TOOLS
from app.tools.schemas import TOOLS_SCHEMA


class AgentService:

    _client = OpenAI()

    @classmethod
    def gather_context(cls, question: str) -> str:
        response = cls._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return ""

        context_parts = []

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            result = TOOLS[function_name](**arguments)
            context_parts.append(
                f"[{function_name}]\n{json.dumps(result, ensure_ascii=False, indent=2)}"
            )

        return "\n\n---\n\n".join(context_parts)
