import flet as ft


class HashSelector(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def item_selected(self, e: ft.TapEvent):
        self.data = e.control.data
        e.control.update()
        self.update()

    def build(self):
        return ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.GRID_GOLDENRATIO_ROUNDED),
                            ft.Text("Average"),
                        ]
                    ),
                    on_click=self.item_selected,
                    data="average"
                ),
            ],
        )