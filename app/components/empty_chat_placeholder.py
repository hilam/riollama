from __future__ import annotations

from typing import *  # type: ignore

import rio

from .. import components as comps, themes


class EmptyChatPlaceholder(rio.Component):
    """
    This component is a placeholder, which is displayed to the user if there is
    no chat history yet. It greets the user, contains suggestions for the user
    to start a conversation, as well as a text input for the user to ask
    anything they have in mind.
    """

    # This will be used for the text input to store its result in
    user_message_text: str = ""

    # This event will be triggered when the user sends a message, be it custom
    # or one of the suggestions.
    on_question: rio.EventHandler[str] = None

    async def on_text_input_confirm(self, *_) -> None:
        """
        Called when the text input is confirmed, or the "send" button pressed.
        The function ensures that the input isn't empty. If that's the case the
        message is sent on to the `on_question` event.
        """
        # If the user hasn't typed anything, do nothing
        message_text = self.user_message_text.strip()

        if not message_text:
            return

        # Trigger the `on_question` event
        await self.call_event_handler(self.on_question, message_text)

    def build(self) -> rio.Component:
        return rio.Column(
                # Explain what the chat is all about
                rio.Text(
                    "Um assistente IA, para lhe auxiliar",
                    justify="center",
                    margin_top=1,
                ),
                # And also give suggestions for them to start with
                rio.Text(
                    "Sugestões",
                    justify="center",
                    style="dim",
                    margin_top=3,
                ),
                rio.Row(
                    comps.ChatSuggestionCard(
                        "material/restaurant",
                        "Sugira formas de fazer um prato ficar mais delicioso",
                        on_press=self.on_question,
                    ),
                    comps.ChatSuggestionCard(
                        "material/coffee",
                        "Qual a melhor maneira de armazenar café?",
                        on_press=self.on_question,
                    ),
                    comps.ChatSuggestionCard(
                        "material/co-present",
                        "Me ajude com a minha apresentação técnica",
                        on_press=self.on_question,
                    ),
                    comps.ChatSuggestionCard(
                        "material/work",
                        "Rascunhe um soneto sobre trabalho",
                        on_press=self.on_question,
                    ),
                    spacing=1,
                    margin_top=1,
                ),
                # Give the user an opportunity to enter a custom question
                rio.Row(
                    rio.MultiLineTextInput(
                        label="Pergunte algo ou forneça uma instrução...",
                        text=self.bind().user_message_text,
                        on_confirm=self.on_text_input_confirm,
                        width="grow",
                        height=5,
                    ),
                    rio.IconButton(
                        "material/navigate-next",
                        on_press=self.on_text_input_confirm,
                    ),
                    spacing=1,
                    margin_top=1,
                ),
                spacing=0.5,
                margin_top=5,
            )
