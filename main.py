import os
import threading
from typing import List, Tuple
import flet as ft
from send2trash import send2trash
from core import SimilarityFinder
from ui.app import DupliApp

from ui.components import FolderPicker, loading_modal, SimilarViewer, failed_delete_banner


similarities: List[Tuple[str, str, int]] = []


def main(page: ft.Page):
    page.title = "Dupli"
    page.window_min_width = 800
    page.window_min_height = 480
    page.padding = 0
    app = DupliApp(page, expand=True,)
    page.add(app)
    page.update()
    app.initialize()

    return

    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)

    page.on_resize = page_resize

    def get_selected_path() -> str:
        session_store = page.session
        if session_store is None:
            return ""
        if session_store.contains_key("selected_path"):
            sel_path = session_store.get("selected_path")
            return sel_path if sel_path is not None else ""
        return ""

    def set_selected_path(path: str):
        if page.session is None:
            return
        page.session.set("selected_path", path)

    def close_banner(e):
        if page.banner is None:
            return
        page.banner.open = False  # type:ignore
        page.update()

    def on_delete_image(img_path: str):
        global similarities
        if not os.path.isfile(img_path) or not os.path.exists(img_path) or img_path == "":
            page.banner = failed_delete_banner(on_retry=lambda _: on_delete_image(
                img_path), on_ignore=close_banner, on_cancel=close_banner)
            page.banner.open = True
            page.update()
            return
        try:
            path_to_delete = img_path.replace("/", "\\")
            if os.path.exists(path_to_delete):
                send2trash(path_to_delete.replace('\\\\?\\', ''))

            show_snackbar(f"{img_path} has been deleted")
            similarities = [
                item for item in similarities if not item.__contains__(img_path)]
            if len(similarities) > 0:
                similar_viewer.visible = True
                similar_viewer.add_data(similarities)
                similar_viewer.update()
            else:
                similar_viewer.visible = False
                similar_viewer.add_data(similarities)
                similar_viewer.update()
                show_snackbar(
                    text="No more duplicates."
                )
                page.update()
        except Exception as e:
            page.banner = failed_delete_banner(on_retry=lambda _: on_delete_image(
                img_path), on_ignore=close_banner, on_cancel=close_banner)
            page.banner.open = True
            show_snackbar(f"{e}")
            page.update()

    similar_viewer = SimilarViewer(on_delete_image)
    similar_viewer.expand = True
    load_modal = loading_modal()

    def show_snackbar(text: str):
        page.snack_bar = ft.SnackBar(
            ft.Text(text)
        )
        page.snack_bar.open = True
        page.update()

    def scan_folder():
        global similarities
        finder = SimilarityFinder()
        similarities = finder.find_similar_images(
            get_selected_path(),
            threshold=1
        )

        if len(similarities) > 0:
            similar_viewer.visible = True
            similar_viewer.add_data(similarities)
            similar_viewer.update()
        else:
            show_snackbar(
                text="The selected path does not have similar images, try changing the similarity threshold."
            )
        load_modal.open = False

        page.update()

    def fab_pressed(e):
        page.dialog = load_modal
        load_modal.open = True
        page.update()
        threading.Thread(
            target=scan_folder,
            args=()
        ).start()

    def on_path_selected(dir_path):
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path) or dir_path == "":
            set_selected_path("")
            show_snackbar(
                f"The selected path is not a directory or does not exist")
            return

        set_selected_path(dir_path)

        page.floating_action_button = ft.FloatingActionButton(
            text="Scan",
            icon=ft.icons.SEARCH_ROUNDED,
            on_click=fab_pressed,
            mini=False,
            autofocus=True
        )
        similar_viewer.clear()
        similar_viewer.visible = False
        similar_viewer.update()

        page.update()

    folder_picker = FolderPicker(on_path_selected)

    main_col = ft.Column(
        [
            folder_picker,
            similar_viewer,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
    page.add(
        main_col
    )
    similar_viewer.visible = False
    page.overlay.append(folder_picker.picker)
    close_banner(None)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
