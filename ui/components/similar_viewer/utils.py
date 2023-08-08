import flet as ft

from core.similarity_finder import get_supported_image

def image_builder(
    image_path: str,
    height: int | None = None,
    width: int | None = None,
    max_size: tuple[int, int] = (500, 500),
    fit: ft.ImageFit = ft.ImageFit.CONTAIN,
    expand: bool | int | None = None
):
    # bytes_img: bytes = isf.get_supported_image(
    #     image_path,
    #     max_size=max_size,
    #     as_b64=True,
    # )  # type: ignore
    str_img: str = get_supported_image(
        image_path,
        max_size=max_size,
        as_b64=False,
    )  # type: ignore
    return ft.Image(
        # src_base64=bytes_img.decode('utf-8'),  # type: ignore
        src=str_img,
        height=height,
        width=width,
        fit=fit, # type: ignore
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(10),
        expand=expand
    )
