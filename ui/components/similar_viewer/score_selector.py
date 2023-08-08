from core.similar_image import SimilarImage


import flet as ft


from typing import Callable, List, OrderedDict

from ui.components.similar_viewer.utils import image_builder


class ScoreTile(ft.UserControl):
    def __init__(
        self,
        on_click: Callable[[ft.TapEvent], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._selected = False
        self._on_click = on_click
        self.list_tile = ft.Container(
            content=self.leading,
            border_radius=ft.border_radius.all(16.0),
            padding=ft.padding.all(12),
            on_click=self.on_click,
            expand=True
        )

    def on_click(self, event: ft.TapEvent):
        self._on_click(event)
        self.selected = True

    @property
    def leading(self):
        return ft.Text(f"{self.data[0]}")

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, status: bool):
        self._selected = status
        if status:
            self.list_tile.bgcolor = ft.colors.PRIMARY_CONTAINER
        else:
            self.list_tile.bgcolor = ft.colors.BACKGROUND
        # self.list_tile.selected = status
        self.list_tile.update()
        self.update()

    def build(self):
        return self.list_tile


class ScoreSelector(ft.UserControl):
    def __init__(
        self,
        similarities: OrderedDict[int, List[SimilarImage]],
        on_score_switch: Callable[[ft.TapEvent], None],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.similarities = similarities
        self.on_score_switch = on_score_switch
        self.current_item = 0
        self.list_view = ft.ListView(
            self.score_list,  # type: ignore
            spacing=0,
            padding=0,
            expand=1,
            data=[]
        )

    @property
    def scores(self):
        scores = [x for x in self.similarities.keys()]
        scores.sort()
        return scores

    @property
    def score_list(self):
        return [
            ScoreTile(
                data=(i, self.similarities[i]),
                on_click=self.on_switch_score  # type: ignore
            ) for i in self.scores
        ]

    def on_switch_score(self, event: ft.TapEvent):
        score_data = event.control.data
        self.on_score_switch(event)
        for item in self.score_list:
            if item.data is score_data:
                self.current_item = self.score_list.index(item)

        if len(self.scores) < 2:
            self.list_view.visible = False
        try:
            self.list_view.update()
        except AssertionError:
            pass
        finally:
            self.update()

    def build(self):
        return ft.Container(
            self.list_view,
            expand=True,
        )
