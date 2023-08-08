from core.similar_image import SimilarImage
from core.similarity_finder import get_supported_image


import flet as ft


from typing import Callable, List, Tuple


class ScoreImageList(ft.UserControl):
    def __init__(
        self,
        score_data: Tuple[int, List[SimilarImage]],
        on_image_selected: Callable[[int], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.score_data = score_data
        self.on_image_selected = on_image_selected
        self.current_item = 0

    @property
    def image_src_list(self):
        for (index, image) in enumerate(self.score_data[1]):
            yield index, get_supported_image(
                image.image_path,
                max_size=(50, 50),
                as_b64=True,
            )

    @property
    def controls_list(self) -> List[ft.Control]:
        return [
            ft.Container(
                image_src_base64=image_data[1].decode('utf-8'),  # type: ignore
                width=50,
                height=50,
                border_radius=ft.border_radius.all(16),  # type: ignore
                scale=ft.transform.Scale(scale=1),
                animate=ft.animation.Animation(
                    300,
                    ft.AnimationCurve.EASE_IN_OUT_EXPO
                ),
                data=image_data,
                on_click=self.on_item_click,
                # on_hover=self.on_item_hover,
                expand=True
            ) for image_data in self.image_src_list
        ]

    def on_item_click(self, event: ft.TapEvent):
        data: Tuple[int, bytes | str] = event.control.data
        self.on_image_selected(data[0])
        self.update()

    def build(self):
        return ft.ListView(
            controls=self.controls_list,
            horizontal=True,
            expand=True
        )