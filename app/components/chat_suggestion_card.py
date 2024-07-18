from __future__ import annotations

from typing import *  # type: ignore

import rio


class ChatSuggestionCard(rio.Component):
    """
    While the chat is empty, a placeholder is displayed. That placeholder
    contains several of these components, which are suggestions for the user to
    start a conversation.
    """

    icon: str
    text: str

    on_press: rio.EventHandler[str] = None

    async def _on_press(self) -> None:
        await self.call_event_handler(self.on_press, self.text)

    def build(self) -> rio.Component:
        # A suggestion is just an icon, text and button wrapped inside a card.
        return rio.Card(
            rio.Column(
                rio.Icon(self.icon),
                rio.Text(
                    self.text,
                    justify="center",
                    wrap=True,
                    height="grow",
                    align_y=0.5,
                ),
                rio.Button(
                    "Use a sugestão",
                    icon="material/navigate-next",
                    style="minor",
                    on_press=self._on_press,
                ),
                spacing=0.6,
                margin=1,
            ),
        )

