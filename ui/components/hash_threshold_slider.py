import flet as ft


from typing import Callable, Optional
from misc.percentage_converter import PercentageConverter


class HashThresholdSlider(ft.UserControl):
    def __init__(
        self,
        on_threshold_change: Callable[[int], None],
        user_friendly: Optional[bool] = True,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_threshold_change = on_threshold_change
        self._user_friendly = user_friendly

        self.converter = PercentageConverter()
        self.slider = ft.Slider(
            min=1,
            max=100,
            divisions=99,
            round=0,
            value=100,
            label="{value}%",
            on_change=self.threshold_changed,
        )
        self.threshold_text = ft.Text(f"{self.slider.value}")

    @property
    def user_friendly(self):
        return self._user_friendly

    @user_friendly.setter
    def user_friendly(self, value: bool):
        self._user_friendly = value
        self.update()

    def threshold_changed(self, event: ft.ControlEvent):
        self.data = int(event.control.value)
        if self.user_friendly:
            real_value = self.converter.pct_to_int(self.data)
            self.on_threshold_change(real_value)
            self.threshold_text.value = f"{self.data}%"
        else:
            self.on_threshold_change(self.data)
            self.threshold_text.value = f"{self.data}"
        self.update()

    def build(self):
        return ft.Container(
            ft.Row(
                [
                    self.slider,
                    self.threshold_text
                ],
                alignment=ft.MainAxisAlignment.END,
                tight=True
            ),
            padding=ft.padding.symmetric(horizontal=10)
        )
