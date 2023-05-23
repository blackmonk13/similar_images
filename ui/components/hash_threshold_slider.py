import flet as ft


from typing import Callable


class HashThresholdSlider(ft.UserControl):
    def __init__(self, on_threshold_change: Callable[[int], None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_threshold_change = on_threshold_change
        self.threshold_text = ft.Text("")

    def threshold_changed(self, event: ft.ControlEvent):
        self.data = event.control.value
        self.on_threshold_change(self.data)
        self.threshold_text.value = self.data
        self.update()

    def build(self):
        return ft.Container(
            ft.Row(
                [
                    ft.Slider(
                        min=1,
                        max=10,
                        divisions=9,
                        # label="{value}",
                        on_change=self.threshold_changed,
                        tooltip="Lower is better."
                    ),
                    self.threshold_text
                ],
                alignment=ft.MainAxisAlignment.END,
                tight=True
            ), 
            padding=ft.padding.symmetric(horizontal=10)
        )
