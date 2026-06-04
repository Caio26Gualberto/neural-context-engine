from app.tools.schemas import TOOLS_SCHEMA
from app.tools.registry import TOOLS

import json

from openai import OpenAI

from app.tools.registry import TOOLS
from app.tools.schemas import TOOLS_SCHEMA


class AgentService:

    _client = OpenAI()

    @classmethod
    def ask(cls, question: str) -> str:

        response = cls._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            tools=TOOLS_SCHEMA,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        tool_call = message.tool_calls[0]

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        result = TOOLS[function_name](**arguments)

        second_response = cls._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": question
                },
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            ]
        )

        return second_response.choices[0].message.content