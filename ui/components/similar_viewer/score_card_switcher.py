from core.similar_image import SimilarImage
from ui.components.similar_viewer.comparison_card import ComparisonCard


import flet as ft


from typing import List, Optional, Tuple


class ScoreCardSwitcher(ft.UserControl):
    def __init__(
        self,
        score_data: Optional[Tuple[int, List[SimilarImage]]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._score_data = score_data
        self.current_item = 0
        self.switcher = ft.AnimatedSwitcher(
            content=ComparisonCard(
                self.image_list[0],
                expand=True
            ) if self.image_list else None,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=300,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
            expand=True,
        )
        self.next_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
            icon_size=20,
            tooltip="Next Image",
            on_click=self.on_next_image
        )
        self.previous_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK_IOS_ROUNDED,
            icon_size=20,
            tooltip="Previous Image",
            on_click=self.on_previous_image
        )

    @property
    def image_list(self) -> List[SimilarImage]:
        return self.score_data[1] if self.score_data is not None else []

    @property
    def score_data(self):
        return self._score_data

    @score_data.setter
    def score_data(self, value: Tuple[int, List[SimilarImage]]):
        self._score_data = value
        try:
            self.update()
        except AssertionError:
            pass
        finally:
            if self.image_list:
                self.switch_to(0)

    def switch_to(self, index: int):
        self.switcher.content = ft.Stack(
            [
                ComparisonCard(
                    self.image_list[index],
                    expand=True,
                ),
                ft.Row(
                    [
                        self.previous_button,
                        self.next_button,
                    ],
                    # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    # top=50,
                    height=50,
                    width=100,
                )
            ],
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            expand=True,
        )
        self.update_buttons()
        try:
            self.switcher.update()
            self.update()
        except AssertionError:
            pass

    def on_previous_image(self, event: ft.TapEvent):
        self.current_item = self.current_item + \
            1 if self.current_item < (len(self.image_list) - 1) else 0
        self.switch_to(self.current_item)

    def on_next_image(self, event: ft.TapEvent):
        self.current_item = self.current_item - \
            1 if self.current_item > 0 else (len(self.image_list) - 1)
        self.switch_to(self.current_item)

    def update_buttons(self):
        if len(self.image_list) < 2:
            self.next_button.visible = False
            self.next_button.disabled = True
            self.previous_button.visible = False
            self.previous_button.disabled = True

    def build(self):
        self.update_buttons()
        return self.switcher
