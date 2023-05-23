from typing import Callable
import flet as ft


class FolderPicker(ft.UserControl):
    def __init__(self, on_path_selected: Callable[[str], None]):
        super().__init__()
        self.on_path_selected = on_path_selected
        self.picker = ft.FilePicker(on_result=self.on_result)
        self.selected_path = ft.Text()

    def on_result(self, event: ft.FilePickerResultEvent):
        self.data = event.path if event.path else ""
        self.selected_path.value = self.data
        self.selected_path.update()
        if event.path:
            self.on_path_selected(event.path)
        self.update()

    def build(self):
        action = "Pick" if self.data is None or self.data == "" else "Change"
        
        return ft.Row(
            [
                self.selected_path,
                ft.ElevatedButton(
                    action + " folder",
                    icon=ft.icons.FOLDER,
                    on_click=lambda _: self.picker.get_directory_path(),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=1,
        )
