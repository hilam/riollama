from pathlib import Path

import rio

from .. import components as comps


class AboutPage(rio.Component):
    def build(self) -> rio.Component:
        return rio.Column(
            comps.HeaderApp(),
            rio.Image(
                Path(self.session.assets / 'llamaCopacabana.png'),
            ),
            rio.Text(
                'Desenvolvido por Hildeberto <hildeberto@gmail.com>'
            )
        )
