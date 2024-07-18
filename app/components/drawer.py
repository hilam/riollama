import rio


class ConfigDrawer(rio.Component):
    ollama_server: str = "http://localhost:11434"
    ollama_model: str = ""
    temperature: float = 0.5
    timeout: int = 5
    max_tokens: int = 500
#    prompt: str
    is_open: bool = False

    def on_press_button(self) -> None:
        self.is_open = True

    def config_content(self) -> rio.Component:
        return rio.Column(
            rio.Text("Configurações", style=rio.TextStyle(font_weight='bold')),
            rio.TextInput(
                label="Servidor Ollama",
                text=self.bind().ollama_server,
            ),
            rio.Dropdown(
                label="Modelo",
                options={
                    "Escolha...": "",
                    "Phi3": "phi3:instruct",
                    "Llama3": "llama3:instruct",
                },
                selected_value=self.bind().ollama_model,
            ),
            rio.Text('Ajuste Temperatura', style=rio.TextStyle(font_weight='bold')),
            rio.Text('(0-mais assertivo, 1-mais criativo)'),
            rio.Slider(
                minimum=0.0,
                maximum=1.0,
                step=0.1,
                value=self.bind().temperature,
                show_values=True,
                # on_change=self.on_change_temp,
            ),
            rio.Text('Tempo máximo de espera', style=rio.TextStyle(font_weight='bold')),
            rio.Text('(em minutos)'),
            rio.Slider(
                minimum=1,
                maximum=10,
                step=1,
                value=self.bind().timeout,
                show_values=True,
                # on_change=self.on_change_time,
            ),
            rio.Text('Tamanho máximo da resposta', style=rio.TextStyle(font_weight='bold')),
            rio.Text('(em tokens)'),
            rio.Slider(
                minimum=100,
                maximum=2000,
                step=50,
                value=self.bind().max_tokens,
                show_values=True,
                # on_change=self.on_change_time,
            ),
            # rio.Text('Prompt padrão', style=rio.TextStyle(font_weight='bold')),
            # rio.ScrollContainer(
            #     rio.Markdown(
            #         text=self.prompt
            #     ),
            #     height=15,
            # ),
            margin=1,
            spacing=1.5,
            align_x=0,
            align_y=0,
        )

    def build(self) -> rio.Component:
        return rio.Drawer(
            anchor=rio.IconButton(
                "material/keyboard-double-arrow-right",
                align_x=0,
                size=2,
                on_press=self.on_press_button,
            ),
            content=self.config_content(),
            is_open=self.is_open,
        )
