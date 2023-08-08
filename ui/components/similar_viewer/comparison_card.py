from core.similar_image import SimilarImage
from core.similarity_finder import get_supported_image
from ui.components.similar_viewer.utils import image_builder


import flet as ft


import os


class ComparisonCard(ft.UserControl):
    def __init__(self, image: SimilarImage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image

    @property
    def image_view(self):
        return image_builder(
            image_path=self.image.image_path,
            expand=True,
        )

    @property
    def delete_button(self):
        # ft.TextButton(
        #     "Delete",
        #     icon=ft.icons.DELETE,
        #     icon_color="red500",
        #     style=ft.ButtonStyle(color="red500",),
        #     # on_click=lambda _:self.delete_image(
        #     #     image_path)
        # )
        return ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            icon_size=20,
            tooltip="Delete Image",
        )

    @property
    def ignore_button(self):
        # ft.TextButton(
        #     "Ignore",
        #     icon=ft.icons.HIDE_IMAGE,
        #     # on_click=lambda _:self.delete_image(
        #     #     image_path)
        # ),
        return ft.IconButton(
            icon=ft.icons.HIDE_IMAGE_ROUNDED,
            icon_color="blue400",
            icon_size=20,
            tooltip="Ignore",
        )

    @property
    def info_view(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            os.path.basename(
                                self.image.image_path),
                            bgcolor=ft.colors.BACKGROUND
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Text(
                            f"{self.image.image_info['dimensions'][0]} x {self.image.image_info['dimensions'][1]}",
                            bgcolor=ft.colors.BACKGROUND
                        ),
                        ft.Text(
                            f"{self.image.image_info['size']}",
                            bgcolor=ft.colors.BACKGROUND
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Text(
                            os.path.dirname(
                                self.image.image_path),
                            bgcolor=ft.colors.BACKGROUND
                        ),
                    ],
                )
            ],
            expand=True
        )

    def build_old(self):
        return ft.Card(
            content=ft.Stack(
                [
                    self.image_view,
                    ft.Row(
                        [
                            self.ignore_button,
                            self.delete_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        # expand=1,
                    ),
                    ft.Row(
                        [
                            self.info_view,

                        ],
                        height=50,
                        width=100,
                        bottom=40,
                        left=5,
                    ),
                ],
                expand=True,
            ),
            expand=True,
        )

    def build(self):
        image_src: str = get_supported_image(
            self.image.image_path,
            max_size=(500,500),
            as_b64=False,
        )  # type: ignore
        return ft.Container(
            image_src=image_src,
            expand=True
        )
