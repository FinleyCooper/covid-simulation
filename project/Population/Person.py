from manim import *
from Population import schedules
import random
import numpy as np
import math
from uuid import uuid4

# np.random.seed(2153)
# random.seed(9453)

INFECTION_DISTANCE_THRESHOLD = 0.05


def get_random_velocity(magnitude):
    theta = PI * 2 * random.random()

    i = math.cos(theta) * magnitude
    j = math.sin(theta) * magnitude

    return np.array([i, j, 0])


class Person(Circle):
    def __init__(self, town=None, home=None, container=None, speed=0.5, radius=0.01, age=None, fill_opacity=1):
        super().__init__(radius=radius, fill_opacity=fill_opacity)

        self._id = uuid4().hex

        self.successful_infections = set()

        self.speed = speed
        self.velocity = get_random_velocity(speed)

        self.susceptible = True
        self.exposed = False
        self.infectious = False
        self.recovered = False

        self.infection_time = None

        self.will_quarantine = False
        self.quarantine_start_time = None

        # Gamma distribution as described in the COVID-19.md doc file
        self.incubation_period = min(np.random.gamma(3.83, 1.64), 13.1)
        self.incubation_period = max(self.incubation_period, 1.401)

        self.latency_period = self.incubation_period - 1.4

        self.asymptomatic = np.random.choice([True, False], p=[0.405, 0.595])

        self.is_showing_symptoms = False

        if self.asymptomatic:
            self.time_to_recover_from_infection = self.latency_period + 6
        else:
            self.time_to_recover_from_infection = self.incubation_period + 10

        self.color = "#1e9efa"  # Blue

        self.age = age
        self.home = home
        self.town = town

        self.set_container(home if container is None else container)

        self.schedule = schedules.assign_schedule(age=self.age, home=self.home, town=town)

        self.current_event = None

        self.add_updater(self.tick)

    def infect(self):
        self.town.on_infection(self)
        self.infection_time = self.town.clock.simulation_seconds
        self.susceptible = False
        self.exposed = True
        self.infectious = False
        self.recovered = False
        self.color = "#fc9403"  # Orange

    def start_infectiousness(self):
        self.susceptible = False
        self.exposed = False
        self.infectious = True
        self.recovered = False
        self.color = "#fc7d74" if self.asymptomatic else "#ff4d4f"

    def recover(self):
        self.town.on_recovery(self)
        self.susceptible = False
        self.exposed = False
        self.infectious = False
        self.recovered = True
        self.color = "#9891a1"  # Grey

    def set_container(self, new_container):
        self.container = new_container
        self.velocity = get_random_velocity(self.speed)
        self.position = self.container.get_random_point()
        self.container.add_person(self)

    def send_home(self):
        self.set_container(self.home)

    def quarantine(self):
        if self.home._id == "retirement_home":
            return

        self.town.quarantined_households.add(self.home._id)

    def tick(self, _, dt):
        # Movement
        self.position += self.velocity * dt
        self.move_to(self.position)

        if self.get_bottom() <= self.container.bottom or self.get_top() >= self.container.top:
            self.velocity[1] = -self.velocity[1]
        if self.get_left_edge() <= self.container.left_edge or self.get_right_edge() >= self.container.right_edge:
            self.velocity[0] = -self.velocity[0]

        # Events
        event_last_tick = self.current_event
        self.current_event = self.schedule.get_current_event(self.town.clock.simulation_seconds)

        if self.current_event != event_last_tick:
            if self.current_event is not None:
                self.set_container(self.current_event["area"])
            else:
                self.send_home()

        # Become infectious after latency period
        if self.exposed:
            if self.infection_time + self.latency_period * 86400 < self.town.clock.simulation_seconds:
                self.start_infectiousness()

        # Recover once time to recover from infection has passed
        if self.infectious:
            if self.infection_time + self.time_to_recover_from_infection * 86400 < self.town.clock.simulation_seconds:
                self.recover()

        # Check if the person should be showing symptoms if the person is infectious, not asymptomatic, and the incubation period has passed
        if self.infectious and not self.asymptomatic:
            if self.infection_time + self.incubation_period * 86400 < self.town.clock.simulation_seconds:
                self.is_showing_symptoms = True
        else:
            self.is_showing_symptoms = False

        # Transmit disease
        if self.infectious:
            for person in self.container.people:
                if person.susceptible or self.town.calc_R0:
                    # Calculate distance between two people using noramlized vector
                    distance = np.linalg.norm(self.position - person.position)

                    if distance < INFECTION_DISTANCE_THRESHOLD:
                        self.container.infect_person(self, person)

        # Quarantine
        if self.will_quarantine and self.infectious and self.is_showing_symptoms:
            self.quarantine()

        # Remove households from quarantine if they have been in quarantine for 14 days
        if self.home._id in self.town.quarantined_households:
            if self.quarantine_start_time is None:
                self.quarantine_start_time = self.town.clock.simulation_seconds

            if self.quarantine_start_time + 14 * 86400 < self.town.clock.simulation_seconds:
                self.town.quarantined_households.remove(self.home._id)

        # Remove events if the household is on the quarantine list
        if self.home._id in self.town.quarantined_households:
            self.schedule.remove_events(14 * 86400)

    def get_top(self):
        return self.get_center()[1] + self.radius

    def get_bottom(self):
        return self.get_center()[1] - self.radius

    def get_right_edge(self):
        return self.get_center()[0] + self.radius

    def get_left_edge(self):
        return self.get_center()[0] - self.radius

    def __repr__(self):
        return f"Person(age={self.age}, home={self.home}, container={self.container}, latency_period={self.latency_period}, incubation_period={self.incubation_period}, asymptomatic={self.asymptomatic}, time_to_recover_from_infection={self.time_to_recover_from_infection}, is_showing_symptoms={self.is_showing_symptoms}, susceptible={self.susceptible}, exposed={self.exposed}, infectious={self.infectious}, recovered={self.recovered}, successful_infections={self.successful_infections})"
