import flet as ft


class FolderPicker(ft.UserControl):
    def __init__(self, on_path_selected):
        super().__init__()
        self.on_path_selected = on_path_selected
        self.current_path = ""
        self.picker = ft.FilePicker(on_result=self.on_result)
        self.selected_path = ft.Text()

    def on_result(self, e: ft.FilePickerResultEvent):
        self.current_path = e.path if e.path else ""
        self.selected_path.value = self.current_path
        self.selected_path.update()
        if e.path:
            self.on_path_selected(e.path)

    def build(self):
        return ft.Row(
            [
                self.selected_path,
                ft.ElevatedButton(
                    "Pick Folder",
                    icon=ft.icons.FOLDER,
                    on_click=lambda _: self.picker.get_directory_path(),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=1,
        )