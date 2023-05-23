import os
from typing import Callable, List, Tuple
import flet as ft


class SimilarViewer(ft.UserControl):
    def __init__(self, on_delete_image: Callable[[str], None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_delete_image = on_delete_image
        self.listview = ft.ListView(
            spacing=10,
            padding=20,
            expand=1,
            data=[]
        )
        self.switcher = ft.AnimatedSwitcher(
            content=ft.Text(""),
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=300,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
            switch_out_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
            expand=3,
        )

        self.current_item = 0

    def clear(self):
        self.listview.controls.clear()
        self.listview.data = []
        self.listview.update()
        self.data = []

    def build_tile_text(self, img_path: str):
        return ft.Text(
            os.path.basename(img_path),
            size=12,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

    def build_tile(self, first_image: str, second_image: str, threshold: int):
        return ft.ListTile(
            leading=self.build_image(
                first_image,
                fit=ft.ImageFit.COVER,
                width=50,
                height=50,
            ),
            title=self.build_tile_text(first_image),
            subtitle=self.build_tile_text(second_image),
            trailing=ft.Text(f"{threshold}"),
            dense=True,
            data=(first_image, second_image, threshold),
            on_click=self.show_comparison
        )

    def build_image(
        self,
        image_path: str,
        height: int | None = None,
        width: int | None = None,
        max_size: tuple[int, int] = (500, 500),
        fit: ft.ImageFit = ft.ImageFit.CONTAIN,
        expand: bool | int | None = None
    ):
        # bytes_img: bytes = get_supported_image(
        #     image_path,
        #     max_size=max_size,
        #     as_b64=True,
        # )  # type: ignore
        return ft.Image(
            src_base64=bytes_img.decode('utf-8'), # type: ignore
            height=height,
            width=width,
            fit=fit,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
            expand=expand
        )

    def delete_image(self, image_path: str):
        self.on_delete_image(image_path)

    def build_image_info(self, image_path: str, data: tuple):
        image = self.build_image(image_path, expand=8)
        # image_info = get_image_info(image_path)
        image_info = {}
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Ignore",
                                    icon=ft.icons.DELETE,
                                    on_click=lambda _:self.delete_image(
                                        image_path)
                                ),
                                ft.TextButton(
                                    "Delete",
                                    icon=ft.icons.DELETE,
                                    icon_color="red500",
                                    style=ft.ButtonStyle(color="red500",),
                                    on_click=lambda _:self.delete_image(
                                        image_path)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            expand=1,
                        ),
                        image,
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PHOTO),
                            # title=ft.Text(os.path.basename(image_path)),
                            subtitle=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                os.path.basename(image_path),
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"{image_info['dimensions'][0]} x {image_info['dimensions'][1]}"
                                            ),
                                            ft.Text(f"{image_info['size']}"),
                                            ft.Text(
                                                f"{image_info['bit_depth']}"),
                                            ft.Text(
                                                f"{image_info['aspect_ratio']}"),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                os.path.dirname(image_path),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            expand=2
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True,
                padding=10,
            ),
            col=6,
        )

    def build_side_by_side(self, data: Tuple[str, str, int]):
        col_1 = self.build_image_info(data[0], data)
        col_2 = self.build_image_info(data[1], data)
        return ft.ResponsiveRow(
            [
                col_1,
                col_2
            ],
            expand=3,
        )

    def show_comparison(self, e: ft.TapEvent):
        for item in self.listview.controls:
            item.selected = False  # type: ignore
        e.control.selected = True
        data = e.control.data
        self.current_item = self.listview.controls.index(e.control)
        self.switcher.content = self.build_side_by_side(data)
        self.switcher.update()
        self.update()

    @staticmethod
    def image_generator(data: List[Tuple[str, str, int]]):
        for item in data:
            yield item[0], item[1], item[2]

    def add_data(self, data: List[Tuple[str, str, int]]):
        self.data = self.image_generator(data)
        self.listview.data = self.data
        self.listview.controls.clear()
        for item in self.data:
            self.listview.controls.append(
                self.build_tile(item[0], item[1], item[2])
            )
        # Set the selection to the next or previous item
        if self.listview.controls:
            next_index = min(self.current_item, len(
                self.listview.controls) - 1)
            print(f"next index {next_index} prevuos index {self.current_item}")
            next_item = self.listview.controls[next_index]
            for item in self.listview.controls:
                item.selected = False  # type: ignore
            next_item.selected = True  # type: ignore
            item_data = next_item.data
            self.current_item = self.listview.controls.index(next_item)
            self.switcher.content = self.build_side_by_side(item_data)
        else:
            self.switcher.content = ft.Text("")

        # Update the UI
        self.switcher.update()
        self.listview.update()
        self.update()

    def build(self):
        return ft.Row(
            [
                self.listview,
                ft.VerticalDivider(
                    width=9,
                    thickness=3
                ),
                self.switcher
            ],
            spacing=0,
            expand=True
        )
