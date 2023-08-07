from manim import *
from Map.constants import *
import numpy as np
import random

# random.seed(5213)
# np.random.seed(7420)


class BaseTransmissionArea(VGroup):
    def __init__(self, name=None, **kwargs):
        super().__init__()

        self._id = None

        self.name = name

        self.container = Rectangle(**kwargs)
        self.add(self.container)

        self.transmission_chance = BASE_TRANSMISSION_CHANCE

        self.recalculate_edges()

        self.people = []

        if name is not None:
            title = Text(name, font_size=25).move_to(
                np.array(
                    [
                        interpolate(self.left_edge, self.right_edge, 0.5),
                        self.top + 0.4,
                        0,
                    ]
                )
            )
            self.add(title)
            self.recalculate_edges()

    def add_person(self, *people):
        for person in people:
            if person not in self.people:
                self.people.append(person)

    def recalculate_edges(self):
        self.left_edge = self.container.get_left()[0] + STROKE_WIDTH
        self.right_edge = self.container.get_right()[0] - STROKE_WIDTH
        self.top = self.container.get_top()[1] - STROKE_WIDTH
        self.bottom = self.container.get_bottom()[1] + STROKE_WIDTH

    def get_random_point(self):
        padding = 0.1
        return np.array(
            [
                np.random.uniform(self.left_edge + padding, self.right_edge - padding),
                np.random.uniform(self.bottom + padding, self.top - padding),
                0,
            ]
        )

    def move_to(self, *args, **kwargs):
        super().move_to(*args, **kwargs)
        self.recalculate_edges()

    def infect_person(self, infected_person, susceptible_person):
        transmission_chance = self.transmission_chance * (1 if infected_person.asymptomatic else 3.85)
        if random.random() < transmission_chance:
            if susceptible_person.town.calc_R0:
                infected_person.successful_infections.add(susceptible_person._id)
            else:
                susceptible_person.infect()

    def __str__(self):
        return self.name if self.name is not None else super().__str__()

    def __repr__(self):
        return self.name if self.name is not None else super().__repr__()


class House(BaseTransmissionArea):
    def __init__(self, _id=None, **kwargs):
        super().__init__(**kwargs)
        self._id = _id

        self.transmission_chance *= 0.035

    def __str__(self):
        return self._id if self._id is not None else super().__str__()

    def __repr__(self):
        return self._id if self._id is not None else super().__repr__()


class WorkSpace(BaseTransmissionArea):
    def __init__(self, _id=None, **kwargs):
        super().__init__(**kwargs)
        self._id = _id

        self.transmission_chance *= 1

    def __str__(self):
        return self._id if self._id is not None else super().__str__()

    def __repr__(self):
        return self._id if self._id is not None else super().__repr__()


class SocialArea(BaseTransmissionArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transmission_chance *= 1.5


class CommunityArea(BaseTransmissionArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transmission_chance *= 1.5


class School(BaseTransmissionArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transmission_chance *= 0.75

    def infect_person(self, infected_person, susceptible_person):
        transmission_chance = self.transmission_chance * (1 if infected_person.asymptomatic else 3.85)

        if random.random() < transmission_chance:
            if susceptible_person.town.calc_R0:
                infected_person.successful_infections.add(susceptible_person._id)
            else:
                susceptible_person.infect()


class RetirementHome(BaseTransmissionArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id = "retirement_home"
        self.transmission_chance *= 1

    def infect_person(self, infected_person, susceptible_person):
        transmission_chance = self.transmission_chance * (1 if infected_person.asymptomatic else 3.85)

        if random.random() < transmission_chance:
            if susceptible_person.town.calc_R0:
                infected_person.successful_infections.add(susceptible_person._id)
            else:
                susceptible_person.infect()
