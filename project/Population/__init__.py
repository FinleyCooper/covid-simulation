from manim import *
from Population.Person import Person
from Population import households, ages
import random

# random.seed(953)


class Population(VGroup):
    def __init__(self, town, number_of_households=0, retirement_home_size=0, speed=0.5):
        super().__init__()
        self.town = town
        homes = households.distribute_households(number_of_households)

        population_size = retirement_home_size

        number_of_children = 0
        number_of_adults = 0
        number_of_elderly = 0

        population_size += homes["one_person"]
        number_of_adults += homes["one_person"]

        population_size += homes["one_person_aged_66_or_over"]
        number_of_elderly += homes["one_person_aged_66_or_over"]

        population_size += homes["couple_family_no_children"] * 2
        number_of_adults += homes["couple_family_no_children"] * 2  # May include elderly

        population_size += homes["couple_family_one_child"] * 3
        number_of_adults += homes["couple_family_one_child"] * 2
        number_of_children += homes["couple_family_one_child"]

        population_size += homes["couple_famliy_two_children"] * 4
        number_of_adults += homes["couple_famliy_two_children"] * 2
        number_of_children += homes["couple_famliy_two_children"] * 2

        population_size += homes["couple_family_three_children"] * 5
        number_of_adults += homes["couple_family_three_children"] * 2
        number_of_children += homes["couple_family_three_children"] * 3

        population_size += homes["lone_parent_one_child"] * 2
        number_of_adults += homes["lone_parent_one_child"]
        number_of_children += homes["lone_parent_one_child"]

        population_size += homes["lone_parent_two_children"] * 3
        number_of_adults += homes["lone_parent_two_children"]
        number_of_children += homes["lone_parent_two_children"] * 2

        population_size += homes["lone_parent_three_children"] * 4
        number_of_adults += homes["lone_parent_three_children"]
        number_of_children += homes["lone_parent_three_children"] * 3

        population_size += homes["couple_family_one_nondependent_child"] * 3
        number_of_adults += homes["couple_family_one_nondependent_child"] * 3

        population_size += homes["lone_parent_one_nondependent_child"] * 2
        number_of_adults += homes["lone_parent_one_nondependent_child"] * 2

        population_ages = ages.distribute_ages(population_size)

        for i in range(retirement_home_size):
            # Assume the oldest people in the simulation are all in the retirement home
            retirement_home_inhabitant = Person(
                speed=speed, town=town, home=town.area.retirement_home, age=population_ages[-i - 1]
            )
            self.add(retirement_home_inhabitant)

        population_ages = population_ages[:-retirement_home_size]

        # Adjust the population ages to agree with the homes
        assert len(population_ages) + retirement_home_size == population_size
        assert number_of_children == len(list(filter(lambda age: age < 18, population_ages)))

        # Adjust adult ages to agree with the homes by moving some adults to elderly
        difference = number_of_adults - len(list(filter(lambda age: 18 <= age < 66, population_ages)))
        assert difference >= 0

        number_of_adults -= difference
        number_of_elderly += difference

        assert number_of_adults == len(list(filter(lambda age: 18 <= age < 66, population_ages)))
        assert number_of_elderly == len(list(filter(lambda age: age >= 66, population_ages)))

        print(f"Number of people  :  {population_size:3}")
        print(f"Number of children:  {number_of_children:3}")
        print(f"Number of adults  :  {number_of_adults:3}")
        print(f"Number of elderly :  {number_of_elderly:3}")

        # Create the people and house them
        taken_houses = 0

        for i in range(homes["one_person"]):
            age = random.choice(list(filter(lambda age: 18 <= age < 66, population_ages)))
            population_ages.remove(age)

            person = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age)
            self.add(person)

        taken_houses += homes["one_person"]

        for i in range(homes["one_person_aged_66_or_over"]):
            age = random.choice(list(filter(lambda age: age >= 66, population_ages)))
            population_ages.remove(age)

            person = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age)
            self.add(person)

        taken_houses += homes["one_person_aged_66_or_over"]

        for i in range(homes["couple_family_no_children"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            self.add(person_1, person_2)

        taken_houses += homes["couple_family_no_children"]

        for i in range(homes["couple_family_one_child"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_3)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            self.add(person_1, person_2, person_3)

        taken_houses += homes["couple_family_one_child"]

        for i in range(homes["couple_famliy_two_children"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_3)
            age_4 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_4)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            person_4 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_4)
            self.add(person_1, person_2, person_3, person_4)

        taken_houses += homes["couple_famliy_two_children"]

        for i in range(homes["couple_family_three_children"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_3)
            age_4 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_4)
            age_5 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_5)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            person_4 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_4)
            person_5 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_5)
            self.add(person_1, person_2, person_3, person_4, person_5)

        taken_houses += homes["couple_family_three_children"]

        for i in range(homes["lone_parent_one_child"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_2)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            self.add(person_1, person_2)

        taken_houses += homes["lone_parent_one_child"]

        for i in range(homes["lone_parent_two_children"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_3)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            self.add(person_1, person_2, person_3)

        taken_houses += homes["lone_parent_two_children"]

        for i in range(homes["lone_parent_three_children"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_3)
            age_4 = random.choice(list(filter(lambda age: age < 18, population_ages)))
            population_ages.remove(age_4)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            person_4 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_4)
            self.add(person_1, person_2, person_3, person_4)

        taken_houses += homes["lone_parent_three_children"]

        for i in range(homes["couple_family_one_nondependent_child"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)
            age_3 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_3)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            person_3 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_3)
            self.add(person_1, person_2, person_3)

        taken_houses += homes["couple_family_one_nondependent_child"]

        for i in range(homes["lone_parent_one_nondependent_child"]):
            age_1 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_1)
            age_2 = random.choice(list(filter(lambda age: 18 <= age, population_ages)))
            population_ages.remove(age_2)

            person_1 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_1)
            person_2 = Person(speed=speed, town=town, home=town.area.housing.houses[taken_houses + i], age=age_2)
            self.add(person_1, person_2)

        taken_houses += homes["lone_parent_one_nondependent_child"]

        assert taken_houses == len(town.area.housing.houses)
