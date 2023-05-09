import flet as ft


def failed_delete_banner(on_retry, on_ignore, on_cancel):
    return ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED,
                        color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Oops, there were some errors while trying to delete the file. What would you like me to do?",
            color="black"
        ),
        actions=[
            ft.TextButton("Retry", on_click=on_retry),
            ft.TextButton("Ignore", on_click=on_ignore),
            ft.TextButton("Cancel", on_click=on_cancel),
        ],
    )