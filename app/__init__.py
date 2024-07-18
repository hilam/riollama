from __future__ import annotations

import os
from pathlib import Path
from typing import *  # type: ignore

import ollama
import rio
from dotenv import load_dotenv

from . import components as comps
from . import pages

load_dotenv()


def on_app_start(app: rio.App):
    # Create the OpenAI client and attach it to the chat
    app.default_attachments.append(ollama.AsyncClient(host=os.getenv('OLLAMA_SERVER')))


ligth_theme = rio.Theme.from_colors(
    primary_color=rio.Color.from_hex("b7be5fff"),
    secondary_color=rio.Color.from_hex("f2cc49ff"),
    background_color=rio.Color.from_hex("edf3c5ff"),
    neutral_color=rio.Color.from_hex("e2d9c2ff"),
    # hud_color=rio.Color.from_hex(""),
    # disabled_color=rio.Color.from_hex(""),
    # success_color=rio.Color.from_hex(""),
    # warning_color=rio.Color.from_hex(""),
    # danger_color=rio.Color.from_hex(""),
    mode="light",
)

dark_theme = rio.Theme.from_colors(
    primary_color=rio.Color.from_hex("3a3217ff"),
    secondary_color=rio.Color.from_hex("b34f4fff"),
    background_color=rio.Color.from_hex("5a5a54ff"),
    neutral_color=rio.Color.from_hex("3a3e3aff"),
    mode="dark",
)

app = rio.App(
    name='RiOllama',
    pages=[
        rio.Page(
            name="Home",
            page_url='',
            build=pages.ChatPage,
        ),
    ],
    on_app_start=on_app_start,
    theme=(ligth_theme, dark_theme,),
    assets_dir=Path(__file__).parent / "assets",
)
