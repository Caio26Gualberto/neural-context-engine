import os
from typing import Generator

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatService:

    @staticmethod
    def _build_messages(question: str, context: str) -> list:
        system_prompt = (
            "Voc\u00ea \u00e9 um assistente interno do Banco Nexus.\n\n"
            "Responda de forma clara, objetiva e profissional.\n\n"
            "Quando houver dados de ferramentas no contexto, utilize-os como fonte oficial.\n\n"
            "N\u00e3o invente informa\u00e7\u00f5es. "
            "Se n\u00e3o houver informa\u00e7\u00e3o suficiente, diga claramente."
        )
        user_content = (
            f"Contexto obtido pelas ferramentas:\n\n{context}\n\nPergunta: {question}"
            if context else question
        )
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

    @staticmethod
    def answer(question: str, context: str = "") -> str:
        messages = ChatService._build_messages(question, context)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )
        return response.choices[0].message.content

    @staticmethod
    def stream_answer(question: str, context: str = "") -> Generator[str, None, None]:
        messages = ChatService._build_messages(question, context)
        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
