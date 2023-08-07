from manim import *


class Clock(VGroup):
    def __init__(self, simulation_speed=1):
        super().__init__()

        self.simulation_speed = simulation_speed

        self.real_time = 0
        self.simulation_seconds = 0

        self.simulation_days = 0

        self.text = Text("Day 0", font_size=30)

        self.text.add_updater(self.tick)
        self.add(self.text)

    def tick(self, mob, dt):
        self.real_time += dt
        self.simulation_seconds += dt * self.simulation_speed

        difference = (days := int(self.simulation_seconds / 86400)) - self.simulation_days

        if difference:
            self.simulation_days = days

            mob.become(
                Text(
                    f"Day {self.simulation_days}",
                    font_size=28,
                )
            )
            self.move_to(self.position)

    def move_to(self, position):
        super().move_to(position)
        self.position = position
