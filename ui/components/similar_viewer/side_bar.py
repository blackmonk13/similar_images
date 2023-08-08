import os
from typing import Callable, Dict, List, OrderedDict, Tuple
import flet as ft
from core.similar_image import SimilarImage
from ui.components.similar_viewer.utils import image_builder


class SideTile(ft.UserControl):
    def __init__(
        self,
        on_click: Callable[[Tuple[SimilarImage, OrderedDict[int, List[SimilarImage]]]], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._selected = False
        self._on_click = on_click
        self.list_tile = ft.Container(
            content=ft.Row(
                [
                    self.leading,
                    ft.Column(
                        [
                            self.title,
                            self.subtitle,
                        ],
                        expand=4,
                    ),
                ],
                expand=True
            ),
            border_radius=ft.border_radius.all(16.0),
            padding=ft.Padding(
                left=20,
                right=20,
                top=10,
                bottom=10
            ),
            on_click=self.on_click,
            expand=True
        )

    @property
    def image(self) -> SimilarImage:
        return self.data[0]

    @property
    def similarities(self) -> OrderedDict[int, List[SimilarImage]]:
        return self.data[1]

    @property
    def sim_count(self):
        return sum([len(x) for x in self.similarities.values()])

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, status: bool):
        self._selected = status
        if status:
            self.list_tile.bgcolor = ft.colors.PRIMARY_CONTAINER
        else:
            self.list_tile.bgcolor = ft.colors.BACKGROUND
        # self.list_tile.selected = status
        self.list_tile.update()
        self.update()

    @property
    def title(self):
        img_path = os.path.splitext(os.path.basename(self.image.image_path))
        title_text = f"{img_path[0][:4]}...{img_path[0][-4:]}{img_path[1] if img_path[1] else ''}"
        return self.build_tile_text(title_text)

    @property
    def subtitle(self):
        return self.build_tile_text(
            f"{self.sim_count} cop{'ies' if self.sim_count > 1 else 'y'}"
        )

    @property
    def leading(self):
        return image_builder(
            self.image.image_path,
            fit=ft.ImageFit.COVER,
            width=50,
            height=50,
            expand=1,
        )

    def on_click(self, event: ft.TapEvent):
        self._on_click(self.data)
        self.selected = True

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
    def __init__(
            self,
            on_tile_click: Callable[[Tuple[SimilarImage, OrderedDict[int, List[SimilarImage]]]], None],
            *args,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.current_item = 0
        self.on_tile_click = on_tile_click
        self.listview = ft.ListView(
            spacing=10,
            padding=20,
            expand=1,
            data=[],
        )

    @property
    def current_item_data(self):
        if len(self.listview.controls) < 1:
            return None
        cur_item = self.listview.controls[self.current_item]
        item_data: Tuple[SimilarImage,
                         OrderedDict[int, List[SimilarImage]]] = cur_item.data
        return item_data

    @staticmethod
    def data_generator(data: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        for item, similarity in data.items():
            yield item, similarity

    def clear(self):
        self.listview.controls.clear()
        self.listview.data = []
        self.listview.update()
        self.data = []

    def on_list_tile_click(self, data: Tuple[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        self.on_tile_click(data)
        for item in self.listview.controls:
            if item.data is data:
                item.selected = True  # type: ignore
                self.current_item = self.listview.controls.index(item)
            else:
                item.selected = False  # type: ignore
        self.listview.update()
        self.update()

    def update_data(self, data: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        self.clear()
        self.data = self.data_generator(data)
        self.listview.data = self.data
        for item in self.data:
            self.listview.controls.append(
                SideTile(
                    data=item,
                    on_click=self.on_list_tile_click
                )
            )
        self.listview.update()

        # Set the selection to the next or previous item
        if self.listview.controls.__len__() > 0:
            next_index = min(self.current_item, len(
                self.listview.controls) - 1)
            # type: ignore
            next_item = self.listview.controls[next_index]
            for item in self.listview.controls:
                item.selected = False  # type: ignore
            next_item.selected = True  # type: ignore

            item_data = next_item.data
            self.on_list_tile_click(item_data)
            self.current_item = self.listview.controls.index(next_item)

        self.listview.update()
        self.update()

    def build(self):
        return self.listview
