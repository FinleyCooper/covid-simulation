# Teachers
# Source - https://explore-education-statistics.service.gov.uk/find-statistics/school-workforce-in-england
# 18.0 students per teacher. We have exactly 36 students in the town, so 2 teachers.
# Hours - 8:30 to 16:30
# 2 Teachers

# Retirement Home Staff
# Source - https://lottie.org/care-guides/the-number-of-uk-care-home-residents/
# England - 1.65 staff per resident
# Wales - 1.24 staff per resident
# Average weighted for population of England and Wales - About 1.5 staff per resident
# 10 in the reitrement home, so 15 staff
# Hours - 8:00 to 16:00
# 15 Retirement Home Staff

# Bar Staff
# 3 Workers - 16:00 to 23:00

# Shop Staff
# 5 Workers - 9:00 to 17:00

# Sports Centre Staff
# 2 Workers - 8:00 to 16:00

# Restaurant Staff
# 7 Workers - 11:00 to 20:30

# Theatre Staff
# Not staffed as shows will be infrequently open

# Club Staff
# 2 Workers - 20:00 to 02:00 (next day)

# Unemployed
# Source - https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/lf24/lms - April - June 2020 - 75.7%
# We will round this to 85% of adults, as this data takes into account 16-17 year olds, who do not work in our simulation.
# 15% of 99 adults ~= 15 adults

# The remaining 48 adults will be work in workspaces, seperated from the general population.

# Workspace 0 - 6:00 to 14:00  - Construction Site          - 10 adults
# Workspace 1 - 8:30 to 16:30  - Hi-tech Engineering Office -  3 adults
# Workspace 2 - 9:00 to 17:00  - Traditional Office Job     - 16 adults
# Workspace 3 - 9:00 to 18:00  - Administration Job         -  8 adults
# Workspace 4 - 10:00 to 19:00 - Warehouse                  -  8 adults
# Workspace 5 - 12:00 to 20:30 - Low interaction work       -  3 adults
import random

# random.seed(3658)


def get_jobs(town):
    # fmt: off
    job_data = [
        {"priority": 1, "start_time": 6 * 60 * 60,   "end_time": 14 * 60 * 60,    "area": town.area.work.work_spaces[0], "workers": 10, "days": [0, 1, 2, 3, 4, 5   ]},
        {"priority": 1, "start_time": 8.5 * 60 * 60, "end_time": 16.5 * 60 * 60,  "area": town.area.work.work_spaces[1], "workers": 3,  "days": [0, 1, 2, 3, 4      ]},
        {"priority": 1, "start_time": 9 * 60 * 60,   "end_time": 17 * 60 * 60,    "area": town.area.work.work_spaces[2], "workers": 16, "days": [0, 1, 2, 3, 4      ]},
        {"priority": 1, "start_time": 9 * 60 * 60,   "end_time": 18 * 60 * 60,    "area": town.area.work.work_spaces[3], "workers": 8,  "days": [0, 1, 2, 3, 4, 5   ]},
        {"priority": 1, "start_time": 10 * 60 * 60,  "end_time": 19 * 60 * 60,    "area": town.area.work.work_spaces[4], "workers": 8,  "days": [0, 1, 2, 3, 4, 5   ]},
        {"priority": 1, "start_time": 12 * 60 * 60,  "end_time": 20.5 * 60 * 60,  "area": town.area.work.work_spaces[5], "workers": 3,  "days": [0, 1, 2, 3, 4, 5   ]},
        {"priority": 1, "start_time": 18 * 60 * 60,  "end_time": 23 * 60 * 60,    "area": town.area.bar,                 "workers": 3,  "days": [0, 1, 2, 3, 4, 5, 6]},
        {"priority": 1, "start_time": 7.5 * 60 * 60, "end_time": 18.5 * 60 * 60,  "area": town.area.shops,               "workers": 5,  "days": [0, 1, 2, 3, 4, 5, 6]},
        {"priority": 1, "start_time": 7.5 * 60 * 60, "end_time": 16.5 * 60 * 60,  "area": town.area.sports_centre,       "workers": 2,  "days": [0, 1, 2, 3, 4, 5, 6]},
        {"priority": 1, "start_time": 11 * 60 * 60,  "end_time": 20.5 * 60 * 60,  "area": town.area.restaurant,          "workers": 7,  "days": [0, 1, 2, 3, 4, 5, 6]},
        {"priority": 1, "start_time": 20 * 60 * 60,  "end_time": 4 * 60 * 60,     "area": town.area.club,                "workers": 3,  "days": [            4, 5   ]},
        {"priority": 1, "start_time": 8 * 60 * 60,   "end_time": 16.5 * 60 * 60,  "area": town.area.retirement_home,     "workers": 15, "days": [0, 1, 2, 3, 4, 5, 6]},
        {"priority": 1, "start_time": 8.5 * 60 * 60, "end_time": 16.5 * 60 * 60,  "area": town.area.school,              "workers": 2,  "days": [0, 1, 2, 3, 4      ]},
        {"priority":-1, "start_time": 0,             "end_time": 0,               "area": "home",                        "workers": 15, "days": [0, 1, 2, 3, 4, 5, 6]},
    ]
    # fmt: on

    jobs = []
    for job in job_data:
        jobs.extend(job for _ in range(job["workers"]))

    return jobs


class Schedule:
    def __init__(self, home=None, town=None):
        self.home = home
        self.town = town
        self.events = []

    def register_event(self, area=None, start_time=None, end_time=None, priority=0):
        self.events.append({"area": area, "start_time": start_time, "end_time": end_time, "priority": priority})

    def get_current_event(self, time):
        # Get the current event with the highest priority
        current_event = None
        for event in self.events:
            if event["start_time"] <= time < event["end_time"]:
                if current_event is None or event["priority"] > current_event["priority"]:
                    current_event = event

        return current_event

    def get_closest_event(self, time):
        closest_event = None
        for event in self.events:
            if event["start_time"] > time:
                if closest_event is None or event["start_time"] < closest_event["start_time"]:
                    closest_event = event
        return closest_event

    def remove_events(self, time, area=None, area_id="blank", priority=1000):
        # Remove all events that are in the given area or have the given _id and start within the given time
        # Do not remove events with a priority higher than the given priority
        # If area is none, remove all events that start within the given time
        current_time = self.town.clock.simulation_seconds

        temp = [
            event
            for event in self.events
            if not (
                event["start_time"] >= current_time
                and event["start_time"] < current_time + time
                and ((area is None and area_id == "blank") or event["area"] == area or event["area"]._id == area_id)
                and event["priority"] < priority
            )
        ]

        self.events = temp


class SchoolSchedule(Schedule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Must be at school from 8:30 AM to 3:30 PM
        self.school_start_time = 8.5 * 60 * 60
        self.school_end_time = 15.5 * 60 * 60

        # Register school as an event on weekdays for the next 12 weeks
        # Also add 10 minutes variance to the start and end times (5 minutes each way)
        for i in range(12):
            week_start_time = i * 7 * 24 * 60 * 60
            for j in range(5):
                day_start_time = week_start_time + j * 24 * 60 * 60
                start_time = self.school_start_time + day_start_time + random.randint(-5 * 60, 5 * 60)
                end_time = self.school_end_time + day_start_time + random.randint(-5 * 60, 5 * 60)
                self.register_event(area=self.town.area.school, start_time=start_time, end_time=end_time, priority=1)

        # Register recreation for the next 12 weeks.
        # Theatre (only on saturday i=5) is 20% likely.
        # Restaurant on weekdays days is 5% likely, but 20% on saturday and sunday.
        # Sports centre is 20% likely per day.
        # Recreation cannot happen at the same time as a job, so priority is 0.
        for j in range(7):
            day_start_time = week_start_time + j * 24 * 60 * 60
            if j == 5:
                if random.randint(0, 4) == 0:
                    # Register theatre
                    start_time = 19 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    end_time = start_time + 2.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(
                        area=self.town.area.theatre, start_time=start_time, end_time=end_time, priority=0
                    )

            if random.randint(0, 19) == 0:
                # Register restaurant
                start_time = 18.5 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                end_time = start_time + 1.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                self.register_event(
                    area=self.town.area.restaurant, start_time=start_time, end_time=end_time, priority=0
                )
            if random.randint(0, 4) == 0:
                # Register sports centre
                start_time = 16 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                self.register_event(
                    area=self.town.area.sports_centre, start_time=start_time, end_time=end_time, priority=0
                )


class WorkSchedule(Schedule):
    def __init__(self, job=None, **kwargs):
        super().__init__(**kwargs)

        # Also add 10 minutes variance to the start and end times (5 minutes each way)
        self.job_start_time = job["start_time"]
        self.job_end_time = job["end_time"] if job["end_time"] > job["start_time"] else job["end_time"] + 24 * 60 * 60
        self.job_area = job["area"] if job["area"] != "home" else self.home
        self.job_days = job["days"]
        self.job_priority = job["priority"]

        # Register events for the next 12 weeks
        for i in range(12):
            # Register job for the next 12 weeks for the days given by job_days
            week_start_time = i * 7 * 24 * 60 * 60
            for j in self.job_days:
                day_start_time = week_start_time + j * 24 * 60 * 60
                start_time = self.job_start_time + day_start_time + random.randint(-5 * 60, 5 * 60)
                end_time = self.job_end_time + day_start_time + random.randint(-5 * 60, 5 * 60)
                self.register_event(
                    area=self.job_area, start_time=start_time, end_time=end_time, priority=self.job_priority
                )

            # Register lunch break for the next 12 weeks.
            # We'll give a chance of 1/2 to have a lunch break on a job day and 1/4 to have a lunch break on a non-job day
            for j in range(7):
                if j in self.job_days:
                    if random.randint(0, 1) == 0:
                        # Register lunch break
                        day_start_time = week_start_time + j * 24 * 60 * 60
                        lunch_start_time = 12 * 60 * 60 + day_start_time + random.randint(-60 * 60, 60 * 60)
                        lunch_end_time = lunch_start_time + 60 * 60 + random.randint(-60 * 60, 60 * 60)

                        # Area is 20% likely to be restaurant, 80% likely to be shops
                        if random.randint(0, 4) == 0:
                            area = self.town.area.restaurant
                        else:
                            area = self.town.area.shops

                        self.register_event(
                            area=area, start_time=lunch_start_time, end_time=lunch_end_time, priority=2
                        )
                else:
                    if random.randint(0, 3) == 0:
                        # Register lunch break
                        day_start_time = week_start_time + j * 24 * 60 * 60
                        lunch_start_time = 12 * 60 * 60 + day_start_time + random.randint(-60 * 60, 60 * 60)
                        lunch_end_time = lunch_start_time + 60 * 60 + random.randint(-60 * 60, 60 * 60)

                        # Area is 10% likely to be restaurant, 90% likely to be shops
                        if random.randint(0, 9) == 0:
                            area = self.town.area.restaurant
                        else:
                            area = self.town.area.shops

                        self.register_event(
                            area=area, start_time=lunch_start_time, end_time=lunch_end_time, priority=2
                        )

            # Register recreation for the next 12 weeks.
            # Theatre (only on saturday i=5) is 20% likely.
            # Restaurant on weekdays days is 5% likely, but 20% on saturday and sunday.
            # Sports centre is 20% likely per day.
            # Bar is 5% likely per day but 20% on friday and saturday.
            # Club is 5% likely on friday and saturday.
            # Shopping is 1/3 chance per day at any time between 10am and 6pm.
            # Visiting retirement home is 1/20 chance per day at any time between 10am and 6pm.
            # Recreation cannot happen at the same time as a job, so priority is 0.

            for j in range(7):
                day_start_time = week_start_time + j * 24 * 60 * 60
                if j == 5:
                    if random.randint(0, 4) == 0:
                        # Register theatre
                        start_time = 19 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                        end_time = start_time + 2.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                        self.register_event(
                            area=self.town.area.theatre, start_time=start_time, end_time=end_time, priority=0
                        )

                if random.randint(0, 19) == 0:
                    # Register restaurant
                    start_time = 18.5 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    end_time = start_time + 1.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(
                        area=self.town.area.restaurant, start_time=start_time, end_time=end_time, priority=0
                    )
                if random.randint(0, 4) == 0:
                    # Register sports centre
                    # Time is random between 8-10am and 4-6pm

                    if random.randint(0, 1) == 0:
                        start_time = 8 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    else:
                        start_time = 16 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)

                    end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(
                        area=self.town.area.sports_centre, start_time=start_time, end_time=end_time, priority=0
                    )

                if j == 4 or j == 5:
                    x = 4
                else:
                    x = 19

                if random.randint(0, x) == 0:
                    # Register bar
                    start_time = random.randint(18, 22) * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(area=self.town.area.bar, start_time=start_time, end_time=end_time, priority=0)

                if j == 4 or j == 5:
                    if random.randint(0, 14) == 0:
                        # Register club
                        start_time = 22 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                        end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                        self.register_event(
                            area=self.town.area.club, start_time=start_time, end_time=end_time, priority=0
                        )

                if random.randint(0, 2) == 0:
                    # Register shopping
                    start_time = random.randint(10, 18) * 60 * 60 + day_start_time + random.randint(-15 * 60, 30 * 60)
                    end_time = start_time + 0.75 * 60 * 60 + random.randint(-15 * 60, 30 * 60)
                    self.register_event(
                        area=self.town.area.shops, start_time=start_time, end_time=end_time, priority=0
                    )

                if random.randint(0, 19) == 0:
                    # Register visiting retirement home
                    start_time = random.randint(10, 18) * 60 * 60 + day_start_time + random.randint(-15 * 60, 30 * 60)
                    end_time = start_time + 0.75 * 60 * 60 + random.randint(-15 * 60, 30 * 60)
                    self.register_event(
                        area=self.town.area.retirement_home, start_time=start_time, end_time=end_time, priority=0
                    )


class RetirementSchedule(Schedule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Register events for the next 12 weeks
        for i in range(12):
            week_start_time = i * 7 * 24 * 60 * 60

            # Register recreation for the next 12 weeks.
            # Theatre (only on saturday i=5) is 25% likely.
            # Restaurant on weekdays days is 5% likely, but 20% on saturday and sunday.
            # Sports centre is 10% likely per day.
            # Bar is 5% likely per day
            # Shopping is 1/3 chance per day at any time between 10am and 6pm.
            # Visiting retirement home is 1/15 chance per day at any time between 10am and 6pm.
            # Recreation cannot happen at the same time as a job, so priority is 0.

            for j in range(7):
                day_start_time = week_start_time + j * 24 * 60 * 60
                if j == 5:
                    if random.randint(0, 3) == 0:
                        # Register theatre
                        start_time = 19 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                        end_time = start_time + 2.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                        self.register_event(
                            area=self.town.area.theatre, start_time=start_time, end_time=end_time, priority=0
                        )

                if random.randint(0, 19) == 0:
                    # Register restaurant
                    start_time = 18.5 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    end_time = start_time + 1.5 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(
                        area=self.town.area.restaurant, start_time=start_time, end_time=end_time, priority=0
                    )
                if random.randint(0, 9) == 0:
                    # Register sports centre
                    # Time is random between 8-10am and 4-6pm

                    if random.randint(0, 1) == 0:
                        start_time = 8 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    else:
                        start_time = 16 * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)

                    end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(
                        area=self.town.area.sports_centre, start_time=start_time, end_time=end_time, priority=0
                    )

                if random.randint(0, 19) == 0:
                    # Register bar
                    start_time = random.randint(18, 22) * 60 * 60 + day_start_time + random.randint(-10 * 60, 10 * 60)
                    end_time = start_time + 1 * 60 * 60 + random.randint(-10 * 60, 10 * 60)
                    self.register_event(area=self.town.area.bar, start_time=start_time, end_time=end_time, priority=0)

                if random.randint(0, 2) == 0:
                    # Register shopping
                    start_time = random.randint(10, 18) * 60 * 60 + day_start_time + random.randint(-15 * 60, 30 * 60)
                    end_time = start_time + 0.75 * 60 * 60 + random.randint(-15 * 60, 30 * 60)
                    self.register_event(
                        area=self.town.area.shops, start_time=start_time, end_time=end_time, priority=0
                    )

                if random.randint(0, 14) == 0:
                    # Register visiting retirement home
                    start_time = random.randint(10, 18) * 60 * 60 + day_start_time + random.randint(-15 * 60, 30 * 60)
                    end_time = start_time + 0.75 * 60 * 60 + random.randint(-15 * 60, 30 * 60)
                    self.register_event(
                        area=self.town.area.retirement_home, start_time=start_time, end_time=end_time, priority=0
                    )


jobs = None


def assign_schedule(age=None, home=None, town=None):
    global jobs
    if jobs is None:
        jobs = get_jobs(town=town)

    if age < 18:
        return SchoolSchedule(home=home, town=town)
    elif age < 66:
        job = jobs.pop(random.randint(0, len(jobs) - 1))

        return WorkSchedule(home=home, town=town, job=job)
    if age >= 66 and home != town.area.retirement_home:
        return RetirementSchedule(home=home, town=town)

    else:
        return Schedule(home=home, town=town)
