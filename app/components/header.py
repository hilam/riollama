from pathlib import Path

import rio

from app import themes


class HeaderApp(rio.Component):

    darken: str = 'material/nightlight:fill'
    lighten: str = 'material/sunny:fill'
    light: bool = True

    async def on_press_button(self) -> None:
        self.light = not self.light
        await themes.update_and_apply_theme(
            self.session,
            {
                "mode": 'light' if self.light else 'dark',
            },
        )
        await self.force_refresh()

    async def about(self) -> None:
        print(self.session.base_url, self.session.active_page_url)
        if self.session.active_page_url == self.session.base_url:
            self.session.navigate_to('about')
        else:
            self.session.navigate_to('/')
        await self.force_refresh()

    def build(self) -> rio.Component:
        return rio.Row(
            rio.Card(
                rio.Image(
                    Path(self.session.assets / 'llamaCopacabana.png'),
                    corner_radius=1,
                    # width=2.5,
                    # height=2.5,
                ),
                on_press=self.about,
            ),
            # rio.Icon(
            #     'material/air:fill',
            #     width=2.5,
            #     height=2.5,
            # ),
            # rio.Icon(
            #     'material/mountain-flag:fill',
            #     width=2.5,
            #     height=2.5,
            # ),
            rio.Text(
                'RiOllama Chatbot',
                style=rio.TextStyle(
                    font_size=3,
                    font_weight="bold",
                    fill=rio.LinearGradientFill(
                        (self.session.theme.secondary_color, 0),
                        (self.session.theme.primary_color, 1),
                    ),
                ),
                justify='center',
            ),
            rio.Button(
                'Tema',
                icon=self.darken if self.light else self.lighten,
                shape='rounded',
                on_press=self.on_press_button,
                is_sensitive=True,
            ),
            margin_top=2,
            margin_left=10,
            margin_right=10,
            spacing=0.5,
            height=4,
            align_y=0,
            proportions=(2, 6.5, 1.5),
        )
