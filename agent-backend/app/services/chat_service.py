import os
from typing import Generator

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatService:

    @staticmethod
    def _build_messages(
        history: list,
        question: str,
        context: str,
    ) -> list:

        system_prompt = (
            "Você é um assistente interno do Banco Nexus.\n\n"
            "Responda de forma clara, objetiva e profissional.\n\n"
            "Quando houver dados de ferramentas no contexto, utilize-os como fonte oficial.\n\n"
            "Não invente informações. "
            "Se não houver informação suficiente, diga claramente."
        )

        user_content = (
            f"Contexto obtido pelas ferramentas:\n\n{context}\n\nPergunta: {question}"
            if context
            else question
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_content,
            }
        )

        return messages

    @staticmethod
    def answer(history: list, question: str, context: str = "") -> str:
        messages = ChatService._build_messages(history, question, context)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )
        return response.choices[0].message.content

    @staticmethod
    def stream_answer(history: list, question: str, context: str = "") -> Generator[str, None, None]:
        messages = ChatService._build_messages(history, question, context)
        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
