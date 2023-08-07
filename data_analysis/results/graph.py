from manim import *
import scipy
import os

directory = "new_uk_30days_results/"

files = os.listdir(directory)

data_files = [file for file in files if file.startswith("infection_log_") and file.endswith(".txt")]

data = [open(f"{directory}{file}", "r").readlines() for file in data_files]

formatted_data = []

for file in data:
    times = []
    infections = []

    for line in file:
        time, infection = line.split(";")
        time, infection = time.split(":")[1], infection[1:]
        time, infection = float(time), int(infection)
        times.append(time / 86400)
        infections.append(infection)

    formatted_data.append([times, infections])


class Results(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Max times and infections throughout all simulations
        max_time = max([max(times) for times, _ in formatted_data])
        max_infections = max([max(infections) for _, infections in formatted_data])

        # Round up to nearest 10
        max_time = (max_time // 10 + 1) * 10
        max_infections = (max_infections // 10 + 1) * 10

        ax = Axes(
            x_range=(0, max_time, 10),
            y_range=(0, 60, 10),
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 22.5},
            color="BLACK",
        )

        # Interpolate lines to make them smoother
        for times, infections in formatted_data:
            line = ax.plot(
                lambda x: scipy.interpolate.interp1d(
                    times,
                    infections,
                    fill_value=[
                        0,
                    ],
                    bounds_error=False,
                )(x),
                color=BLUE,
                stroke_width=2,
                x_range=(0, max_time, 0.1),
            )

            self.add(line)

        title = Text("UK Policy | 30 days | 8 Trials", font_size=25, color="BLACK")
        title.next_to(ax, UP)

        x_label = ax.get_x_axis_label("t\\text{ (days)}", edge=UR, direction=DR, buff=MED_LARGE_BUFF)
        y_label = ax.get_y_axis_label("\\text{Infections}", edge=UL, direction=UL, buff=MED_LARGE_BUFF)

        x_label.set_color(BLACK)
        y_label.set_color(BLACK)
        ax.set_color(BLACK)

        # self.add(mean)
        self.add(ax, x_label, y_label, title)
