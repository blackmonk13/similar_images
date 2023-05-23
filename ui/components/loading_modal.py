import flet as ft

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


def loading_modal():
    load_indicator = LoadingRing()
    return ft.AlertDialog(
        modal=True,
        content=load_indicator
    )