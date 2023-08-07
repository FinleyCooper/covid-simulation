import settings
import Map
from manim import *
from Population import Population
import random
import Policy

# time = 2000

# Remove all random.seed() calls to make the simulation random

_id = random.randint(0, 1000000000)

# random.seed(534)


class CalcR0(Scene):
    def construct(self):
        town = Map.create_map(calc_R0=True)

        for area in town.area:
            self.add(area)

        self.add(town.clock)

        population = Population(
            town,
            number_of_households=settings.NUMBER_OF_HOUSEHOLDS,
            retirement_home_size=settings.FIXED_RETIREMENT_HOME_SIZE,
            speed=(Map.constants.SIMULATION_SPEED * settings.PERSON_SPEED_PROP_CONSTANT),
        )

        self.add(population)

        # Infect the entire population
        for person in population:
            person.infect()

        # Max inc. period is 13.1 days, and infectious period is 10 days so wait 23.1 days = 23.1 * 24 * 60 * 60 = 1995840 seconds ≈ 2000000 seconds
        time = 2000000 // Map.constants.SIMULATION_SPEED

        print(f"Running simulation for {time} seconds...")

        self.wait(time)

        # Calculate average infections that each person has made
        infections = 0
        for person in population:
            if not person.recovered:
                print(f"ERROR: Person {person} has not recovered")

            print(f"Person has infected {len(person.successful_infections)} people")
            infections += len(person.successful_infections)

        average_infections = infections / len(population)

        print(f"Average infections: {average_infections}")

        # Write R0 to a file
        with open("R0.txt", "a") as f:
            f.write(f"{average_infections}\n")


class Simulation(Scene):
    def construct(self):
        # print(f"Rendering a {time} second simulation...")

        # simulation_time = time * Map.constants.SIMULATION_SPEED
        # simulation_days = simulation_time // 86400
        # simulation_hours = (simulation_time % 86400) // 3600

        # print(
        #     f"Simulation time: {simulation_days} day{'s' if simulation_days != 1 else ''} and {simulation_hours} hour{'s' if simulation_hours != 1 else ''}"
        #     + "\n\n"
        # )

        infection_log = open(f"infection_log_{_id}.txt", "a")

        def log_infection(person):
            infected = 0

            for person in population:
                if person.exposed or person.infectious:
                    infected += 1

            infection_log.write(f"t:{person.town.clock.simulation_seconds:.1f};i{infected}" + "\n")

        town = Map.create_map(on_infection=log_infection, on_recovery=log_infection)

        for area in town.area:
            self.add(area)

        self.add(town.clock)

        population = Population(
            town,
            number_of_households=settings.NUMBER_OF_HOUSEHOLDS,
            retirement_home_size=settings.FIXED_RETIREMENT_HOME_SIZE,
            speed=(Map.constants.SIMULATION_SPEED * settings.PERSON_SPEED_PROP_CONSTANT),
        )

        first_policy_time = 30
        second_policy_time = 1
        third_policy_time = 100 - second_policy_time - first_policy_time
        total_time = first_policy_time + second_policy_time

        policy_list = Policy.create_english_policy(
            first_policy_time,
            second_policy_time,
            third_policy_time,
        )

        print("\n" + f"Running simulation for {total_time} days..." + "\n")
        print(f"No policy: starting on Day 0")
        print(f"First policy: starting on Day {first_policy_time}")
        print(f"Second policy: starting on Day {first_policy_time + second_policy_time}")
        print(f"End of simulation: Day {total_time}" + "\n")

        self.add(population)

        # Choose 3 random patient zeros
        patient_indexes = random.sample(range(0, len(population)), 3)
        for index in patient_indexes:
            population[index].infect()

        while policy_list.active:
            policy, time = policy_list.get_current_policy(population.town.clock.simulation_seconds)
            population = policy.apply(population, time)

            self.wait(time / Map.constants.SIMULATION_SPEED)

        infection_log.close()

        infected = 0
        recovered = 0
        susceptible = 0

        for person in population:
            if person.exposed or person.infectious:
                infected += 1
            elif person.recovered:
                recovered += 1
            else:
                susceptible += 1

        print(f"Infected: {infected}")
        print(f"Recovered: {recovered}")
        print(f"Susceptible: {susceptible}")
