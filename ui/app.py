from typing import Any, Callable, List, Optional, OrderedDict, Union
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


class OptionsDialog(ft.AlertDialog):
    def __init__(
        self,
        on_close,
        on_scan: Callable[[int], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.on_close = on_close
        self.on_scan = on_scan
        self.title = ft.Text("Options")
        self.selected_threshold = 1
        self.content = self.scan_options
        self.actions = [self.scan_button, self.cancel_button]
        self.actions_alignment = ft.MainAxisAlignment.END

    @property
    def scan_options(self):
        return ft.Column(
            [
                HashThresholdSlider(
                    on_threshold_change=self.on_threshold_change
                ),
            ],
            height=100,
            alignment=ft.MainAxisAlignment.CENTER
        )

    @property
    def scan_button(self):
        return ft.TextButton("Scan", on_click=self.on_scan_click)

    @property
    def cancel_button(self):
        return ft.TextButton("Cancel", on_click=self.on_close)
    
    def set_loading(self, loading:bool):
        if loading:
            self.actions = None
            self.title = None
            self.content = LoadingRing()
        else:
            self.actions = [self.scan_button, self.cancel_button]
            self.title = ft.Text("Options")
            self.content = self.scan_options
        self.update()
        

    def on_threshold_change(self, threshold: int):
        self.selected_threshold = threshold
        self.update()

    def on_scan_click(self, event: ft.TapEvent):
        self.set_loading(True)
        self.on_scan(self.selected_threshold)
        self.set_loading(False)
        self.on_close(event)



class LoadingRing(ft.UserControl):
    def build(self):
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text("Please Wait...")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            height=100
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
            on_back=self.on_back,
            expand=True,
        )
        self.folder_picker = FolderPicker(self.on_path_selected)
        self.selected_path = ""
        self.page.overlay.append(self.folder_picker.picker)
        self.options_modal = OptionsDialog(
            on_close=self.on_close_options,
            on_scan=self.on_scan
        )
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
        self.data_store.similarities = OrderedDict()
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

    def show_options(self, open: bool = True):
        if open:
            self.page.dialog = self.options_modal
        self.options_modal.open = open
        try:
            self.options_modal.update()
        except AssertionError:
            pass
        self.page.update()

    def on_back(self, event: ft.TapEvent):
        self.page.go("/")

    def on_close_options(self, event: ft.TapEvent):
        self.show_options(False)

    def on_scan(self, options: int):
        self.data_store.similarities = self.finder.find_similar_images(
            self.selected_path,
            threshold=options
        )
        # print(path)
        # print(self.data_store.similarities)
        if len(self.data_store.similarities) > 0:
            self.page.go("/similarities")
        else:
            self.show_snackbar(
                text="The selected path does not have similar images, try changing the similarity threshold."
            )

    def on_path_selected(self, path: str):
        self.show_options(True)
        self.selected_path = path
        self.update()
        self.page.update()

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
        self.appbar = ft.AppBar(
            title=ft.Text(f"Dupli", size=20,),
            center_title=False,
            # toolbar_height=80,
            automatically_imply_leading=True,
            # bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def route_change(self, event: ft.RouteChangeEvent):
        troute = ft.TemplateRoute(self.page.route)  # type: ignore
        if troute.match("/"):
            self.layout.set_picker_view()
        elif troute.match("/similarities"):
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
