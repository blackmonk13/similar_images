from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from core.similarity_finder import SimilarityFinder
from store.data_store import DataStore

from ui.components import (
    FolderPicker,
    HashThresholdSlider,
    loading_modal
)
from ui.components import SimilarViewer


class SimilarityViewer(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        return ft.ListView(
            [
                ft.ListTile(
                    title=ft.Text(f"{i}")
                ) for i in range(100)
            ],
            expand=True
        )


class AppLayout(ft.UserControl):
    def __init__(self, app, page: ft.Page, data_store: DataStore, finder: SimilarityFinder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page: ft.Page = page
        self.finder = finder
        self.data_store = data_store
        self.similar_viewer = SimilarViewer(
            on_delete_image=lambda _: print(_),
            expand=True,)
        self.folder_picker = FolderPicker(self.on_path_selected)
        self.page.overlay.append(self.folder_picker.picker)
        self.load_modal = loading_modal()
        self.folder_picker_view = ft.Column(
            [
                self.folder_picker
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self._active_view: ft.Control = self.folder_picker_view

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view: ft.Control):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()

    def set_picker_view(self):
        self.active_view = self.folder_picker_view
        self.page.update()

    def set_similarities_view(self):
        self.active_view = self.similar_viewer
        self.similar_viewer.update_data(self.data_store.similarities)
        self.similar_viewer.update()
        self.page.update()

    def show_snackbar(self, text: str):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(text)
        )
        self.page.snack_bar.open = True
        self.page.update()

    def show_loading(self, open: bool = True):
        if self.page.dialog is not self.load_modal:
            self.page.dialog = self.load_modal
        self.load_modal.open = open
        self.page.update()

    def on_path_selected(self, path: str):
        self.show_loading(True)
        self.data_store.similarities = self.finder.find_similar_images(
            path,
            threshold=1
        )
        print(path)
        print(self.data_store.similarities)
        if self.data_store.similarities:
            self.page.go("/similarities")
        else:
            self.show_snackbar(
                text="The selected path does not have similar images, try changing the similarity threshold."
            )
        self.show_loading(False)

    def build(self):
        return ft.Column(
            [
                self.active_view,
            ],
        )


class DupliApp(ft.UserControl):
    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page: ft.Page = page
        self.finder = SimilarityFinder()
        self.data_store = DataStore()
        self.page.on_route_change = self.route_change
        self.threshold_slider = HashThresholdSlider(
            on_threshold_change=lambda _: print(f"Threshold is {_}"),
            visible=False,
        )
        self.appbar = ft.AppBar(
            title=ft.Text(f"Dupli", size=20,),
            center_title=False,
            toolbar_height=80,
            automatically_imply_leading=True,
            # bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                self.threshold_slider,
            ],
        )
        # self.page.appbar = self.appbar
        self.page.update()

    def route_change(self, event: ft.RouteChangeEvent):
        troute = ft.TemplateRoute(self.page.route)  # type: ignore
        if troute.match("/"):
            self.layout.set_picker_view()
        elif troute.match("/similarities"):
            self.threshold_slider.visible = True
            self.layout.set_similarities_view()
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            data_store=self.data_store,
            finder=self.finder,
            expand=True,
        )
        return self.layout

    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    # self.appbar,
                    self.layout
                ],
                padding=ft.padding.all(0),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        self.page.update()
        self.page.go("/")
