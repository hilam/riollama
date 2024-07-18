from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import *  # type: ignore

import ollama


@dataclass
class ChatMessage:
    """
    A simple storage class containing all the information needed for a single
    chat message.
    """

    role: Literal["user", "assistant"]
    timestamp: datetime
    text: str


@dataclass
class Conversation:
    """
    The start of the show. This class contains a list of messages and can
    connect to OpenAI to generate smart responses to the user's messages.
    """

    # The entire message history
    messages: List[ChatMessage] = field(default_factory=list)

    async def respond(
            self, client: ollama.AsyncClient,
            model: str,
            temperature: float = 0.1,
            max_tokens: int = 500,
    ) -> ChatMessage:
        """
        Creates an AI generated response for this conversation and appends it
        to the messages list. Also returns the new message.

        ## Raises

        `ValueError` if the most recent message is not by the user.
        """

        # Make sure the last message was by the user
        if not self.messages or self.messages[-1].role != "user":
            raise ValueError("The most recent message must be by the user")

        # Convert all messages to the format needed by the API
        api_messages: list[Any] = [
            {
                "role": "system",
                "content": "Você é um assistente gentil e prestativo. Responda as questões "
                            "e siga as instruções do usuário de maneira precisa. "
                            "Formate suas respostas em markdown, por exemplo usando "
                            "**negrito**, _itálico_, entre outros.",
            }
        ] + [
            {
                "role": message.role,
                "content": message.text,
            }
            for message in self.messages
        ]

        # Generate a response
        api_response = await client.chat(
            model=model,
            messages=api_messages,
            options={
                'num_predict': max_tokens,
                'temperature': temperature,
            },
        )

        assert isinstance(api_response['message']['content'], str)

        response = ChatMessage(
            role="assistant",
            timestamp=datetime.now(tz=timezone.utc),
            text=api_response['message']['content'],
        )

        # Append the message and return it as well
        self.messages.append(response)

        return response