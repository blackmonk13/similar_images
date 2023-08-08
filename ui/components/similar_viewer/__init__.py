import os
from typing import Callable, Dict, List, OrderedDict, Tuple
import flet as ft

from core import SimilarityFinder as isf
from core.similar_image import SimilarImage
from core.similarity_finder import get_supported_image
from ui.components.hash_threshold_slider import HashThresholdSlider
from ui.components.similar_viewer.comparison_viewer import ComparisonViewer

from .side_bar import SideBar
from .utils import *


class SimilarViewer(ft.UserControl):
    def __init__(
        self,
        on_delete_image: Callable[[str], None],
        on_back: Callable[[ft.TapEvent], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_delete_image = on_delete_image
        self.on_back = on_back
        self.sidebar = SideBar(
            expand=1,
            on_tile_click=self.on_tile_click,
        )
        self.comparison_viewer = ComparisonViewer(
            expand=4,
        )

    def on_tile_click(self, data: Tuple[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        self.comparison_viewer.switch_to(data)

    def update_data(self, data: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        self.data = data
        self.sidebar.update_data(self.data)
        # if self.sidebar.current_item_data:
        #     self.comparison_viewer.switch_to(self.sidebar.current_item_data)
        self.update()

    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK_ROUNDED,
                            icon_size=20,
                            tooltip="Back",
                            on_click=self.on_back
                        ),
                        ft.IconButton(
                            icon=ft.icons.SETTINGS_ROUNDED,
                            icon_size=20,
                            tooltip="Settings",
                            # on_click=self.on_previous_image
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    
                ),
                ft.Row(
                    [
                        self.sidebar,
                        self.comparison_viewer
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
