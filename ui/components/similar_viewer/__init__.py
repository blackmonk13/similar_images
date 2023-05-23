import os
from typing import Callable, Dict, List, Tuple
import flet as ft

from core import SimilarityFinder as isf
from core.similar_image import SimilarImage
from core.similarity_finder import get_supported_image
from ui.components.hash_threshold_slider import HashThresholdSlider


def image_builder(
    image_path: str,
    height: int | None = None,
    width: int | None = None,
    max_size: tuple[int, int] = (500, 500),
    fit: ft.ImageFit = ft.ImageFit.CONTAIN,
    expand: bool | int | None = None
):
    # bytes_img: bytes = isf.get_supported_image(
    #     image_path,
    #     max_size=max_size,
    #     as_b64=True,
    # )  # type: ignore
    str_img: str = get_supported_image(
        image_path,
        max_size=max_size,
        as_b64=False,
    )  # type: ignore
    return ft.Image(
        # src_base64=bytes_img.decode('utf-8'),  # type: ignore
        src=str_img,
        height=height,
        width=width,
        fit=fit,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(10),
        expand=expand
    )


class SideTile(ft.UserControl):
    def __init__(
        self, 
        on_click: Callable[[ft.TapEvent], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._selected = False
        self.on_click = on_click
        self.list_tile = ft.ListTile(
            leading=image_builder(
                self.image.image_path,
                fit=ft.ImageFit.COVER,
                width=50,
                height=50,
            ),
            title=self.build_tile_text(self.image.image_path),
            subtitle=self.build_tile_text(f"{self.similarities.__len__()}"),
            # trailing=ft.Text(f"{self.data[2]}"),
            dense=True,
            selected=self.selected,
            on_click=self.on_click
        )
    @property
    def image(self) -> SimilarImage:
        return self.data[0]
    
    @property
    def similarities(self) -> Dict[int, List[SimilarImage]]:
        return self.data[1]
        
    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, status:bool):
        self._selected = status
        self.list_tile.update()
        self.update()
        
    def build_tile_text(self, img_path: str):
        return ft.Text(
            os.path.basename(img_path),
            size=12,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

    def build(self):
        return self.list_tile


class SideBar(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_item = 0
        self.listview = ft.ListView(
            spacing=10,
            padding=20,
            expand=1,
            data=[]
        )

    @staticmethod
    def data_generator(data: Dict[SimilarImage, Dict[int, List[SimilarImage]]]):
        for item, similarity in data.items():
            yield item, similarity

    def clear(self):
        self.listview.controls.clear()
        self.listview.data = []
        self.listview.update()
        self.data = []

    def on_list_tile_click(self, event:ft.TapEvent):
        data = event.control.data
        for item in self.listview.controls:
            if item.data == data:
                item.selected = True  # type: ignore
                self.current_item = self.listview.controls.index(item)
            else:
                item.selected = False  # type: ignore
        self.listview.update()
        self.update()

    def update_data(self, data: Dict[SimilarImage, Dict[int, List[SimilarImage]]]):
        self.clear()
        self.data = self.data_generator(data)
        self.listview.data = self.data
        for item in self.data: 
            self.listview.controls.append(
                SideTile(
                    data=item,
                    on_click=self.on_list_tile_click  # type: ignore
                )
            )
        self.listview.update()

        # Set the selection to the next or previous item
        if self.listview.controls.__len__() > 0:
            next_index = min(self.current_item, len(
                self.listview.controls) - 1)
            print(f"next index {next_index} prevuos index {self.current_item}")
            next_item:SideTile = self.listview.controls[next_index] # type: ignore
            for item in self.listview.controls:
                item.selected = False  # type: ignore
            next_item.selected = True  # type: ignore
            item_data = next_item.data
            print(item_data)
            self.current_item = self.listview.controls.index(next_item)
        self.listview.update()
        self.update()

    def build(self):
        return self.listview


class SimilarViewer(ft.UserControl):
    def __init__(
        self,
        on_delete_image: Callable[[str], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_delete_image = on_delete_image
        self.sidebar = SideBar(expand=True)

    def update_data(self, data: Dict[SimilarImage, Dict[int, List[SimilarImage]]]):
        self.data = data
        self.sidebar.update_data(self.data)
        self.update()

    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        HashThresholdSlider(
                            on_threshold_change=lambda _:print(_),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    [
                        self.sidebar,
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
