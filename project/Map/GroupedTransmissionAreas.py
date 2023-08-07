from manim import *
from Map.constants import STROKE_WIDTH
from Map.TransmissionAreas import House, WorkSpace


class Housing(VGroup):
    def __init__(self, name="Housing"):
        super().__init__()

        self.houses = [House(width=0.38, height=0.38, _id=f"house_{i}") for i in range(70)]

        self.add(*self.houses)

        self.arrange_in_grid(rows=7, cols=10, buff=0.13)

        self.recalculate_edges()

        if name is not None:
            title = Text(name, font_size=25).move_to(
                np.array(
                    [
                        interpolate(self.left_edge, self.right_edge, 0.5),
                        self.top + 0.36,
                        0,
                    ]
                )
            )
            self.add(title)
            self.recalculate_edges()

    def recalculate_edges(self):
        self.left_edge = self.get_left()[0] + STROKE_WIDTH
        self.right_edge = self.get_right()[0] - STROKE_WIDTH
        self.top = self.get_top()[1] - STROKE_WIDTH
        self.bottom = self.get_bottom()[1] + STROKE_WIDTH

    def move_to(self, *args, **kwargs):
        super().move_to(*args, **kwargs)
        for house in self.houses:
            house.recalculate_edges()
        self.recalculate_edges()

    def __str__(self):
        return self.name if self.name is not None else super().__str__()

    def __repr__(self):
        return self.name if self.name is not None else super().__repr__()


class Work(VGroup):
    def __init__(self, name="Work"):
        super().__init__()

        self.work_spaces = [WorkSpace(width=2.5, height=1.38, _id=f"workspace_{i}") for i in range(6)]

        self.add(*self.work_spaces)

        self.arrange_in_grid(rows=2, cols=3, buff=0.25)

        self.recalculate_edges()

        if name is not None:
            title = Text(name, font_size=25).move_to(
                np.array(
                    [
                        interpolate(self.left_edge, self.right_edge, 0.5),
                        self.top + 0.36,
                        0,
                    ]
                )
            )
            self.add(title)
            self.recalculate_edges()

    def recalculate_edges(self):
        self.left_edge = self.get_left()[0] + STROKE_WIDTH
        self.right_edge = self.get_right()[0] - STROKE_WIDTH
        self.top = self.get_top()[1] - STROKE_WIDTH
        self.bottom = self.get_bottom()[1] + STROKE_WIDTH

    def move_to(self, *args, **kwargs):
        super().move_to(*args, **kwargs)
        for work_spaces in self.work_spaces:
            work_spaces.recalculate_edges()

        self.recalculate_edges()

    def __str__(self):
        return self.name if self.name is not None else super().__str__()

    def __repr__(self):
        return self.name if self.name is not None else super().__repr__()
