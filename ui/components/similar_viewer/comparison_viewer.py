from typing import List, Optional, OrderedDict, Tuple
import flet as ft

from core.similar_image import SimilarImage
from ui.components.similar_viewer.score_image_list import ScoreImageList
from ui.components.similar_viewer.score_selector import ScoreSelector
from ui.components.similar_viewer.score_card_switcher import ScoreCardSwitcher
from ui.components.similar_viewer.comparison_card import ComparisonCard

import flet as ft

from ui.components.similar_viewer.utils import image_builder


class ComparisonViewer(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.switcher = self.build_switcher(
            content=ft.Container(),
        )
        self.score_switcher = self.build_switcher(
            expand=7,
        )
        self.imagelist_switcher = self.build_switcher(
            expand=1
        )
        self.score_card = ScoreCardSwitcher(
            expand=True
        )

    @staticmethod
    def build_switcher(
        content: Optional[ft.Control] = None,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=150,
        reverse_duration=150,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT_EXPO,
        expand: Optional[bool | int] = True,
    ):
        return ft.AnimatedSwitcher(
            content=content,
            transition=transition,
            duration=duration,
            reverse_duration=reverse_duration,
            switch_in_curve=switch_in_curve,
            switch_out_curve=switch_out_curve,
            expand=expand,
        )

    def on_image_selected(self, value: int):
        self.score_card.switch_to(value)
        self.update()

    def switch_to(self, item: Tuple[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        scores = [x for x in item[1].keys()]
        scores.sort()

        self.score_card.score_data = (scores[0], item[1][scores[0]])
        self.score_switcher.content = self.score_card

        self.imagelist_switcher.content = ScoreImageList(
            (scores[0], item[1][scores[0]]),
            on_image_selected=self.on_image_selected
        )

        comp_card = ComparisonCard(
            item[0],
            expand=7,
        )

        score_selector = ScoreSelector(
            similarities=item[1],
            on_score_switch=self.on_switch_score,
            expand=1,
        )

        self.switcher.content = ft.Column(
            [
                self.imagelist_switcher,
                ft.Row(
                    [
                        comp_card,
                        self.score_switcher,
                        score_selector if len(scores) > 1 else ft.Container(),
                    ],
                    expand=9
                ),
            ],
            expand=True,
        )

        # self.score_switcher.update()
        self.switcher.update()
        self.update()

    def on_switch_score(self, event: ft.TapEvent):
        score_data = event.control.data
        self.score_card.score_data = score_data
        self.score_switcher.content = self.score_card

        self.imagelist_switcher.content = ScoreImageList(
            score_data,
            on_image_selected=self.on_image_selected
        )

        self.imagelist_switcher.update()
        self.score_switcher.update()
        self.update()

    def build(self):
        return self.switcher

