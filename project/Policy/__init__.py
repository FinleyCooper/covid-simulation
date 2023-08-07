import random

# random.seed(34521)


class Policy:
    def __init__(self):
        pass


class NoPolicy(Policy):
    def __init__(self):
        super().__init__()

    def apply(self, population, time):
        return population


class ReduceShopping(Policy):
    def __init__(self, shopping_reduction=1):
        self.shopping_reduction = shopping_reduction
        super().__init__()

    def apply(self, population, time):
        end_time = time + population.town.clock.simulation_seconds
        for person in population:
            if random.random() < self.shopping_reduction:
                person.schedule.remove_events(end_time, area=population.town.area.shops)

        return population


class RemoveRetirementHomeVisitingEvents(Policy):
    def __init__(self):
        super().__init__()

    def apply(self, population, time):
        end_time = time + population.town.clock.simulation_seconds

        for person in population:
            person.schedule.remove_events(end_time, area=population.town.area.retirement_home, priority=1)

        return population


# Delete theatre, club, bar, sports centre events
class RemoveSocialEvents(Policy):
    def __init__(self):
        super().__init__()

    def apply(self, population, time):
        end_time = time + population.town.clock.simulation_seconds
        for person in population:
            person.schedule.remove_events(end_time, area=population.town.area.theatre)
            person.schedule.remove_events(end_time, area=population.town.area.club)
            person.schedule.remove_events(end_time, area=population.town.area.bar)
            person.schedule.remove_events(end_time, area=population.town.area.sports_centre)

        return population


# Remove work events from the given workspaces
class WorkFromHome(Policy):
    def __init__(self, workspaces):
        self.workspaces = workspaces
        super().__init__()

    def apply(self, population, time):
        end_time = time + population.town.clock.simulation_seconds

        for person in population:
            for workspace in self.workspaces:
                person.schedule.remove_events(end_time, area_id=workspace)

        return population


# Remove 90% of the events from the school
class ReduceSchoolAttendance(Policy):
    def __init__(self, school_reduction=0.1):
        self.school_reduction = school_reduction
        super().__init__()

    def apply(self, population, time):
        end_time = time + population.town.clock.simulation_seconds
        for person in population:
            if random.random() < self.school_reduction:
                person.schedule.remove_events(end_time, area=population.town.area.school)

        return population


class MasksInShops(Policy):
    def __init__(self, mask_reduction=0.34):
        self.mask_reduction = mask_reduction
        super().__init__()

    def apply(self, population, time):
        for person in population:
            for area in person.town.area:
                if area.name == "Shops":
                    for x in area.shops:
                        x.transmission_chance *= self.mask_reduction
                else:
                    area.transmission_chance *= 1

        return population


class SocialDistancing(Policy):
    def __init__(self, tranmission_chance_reduction=0.5):
        self.transmission_chance_reduction = tranmission_chance_reduction
        super().__init__()

    def apply(self, population, time):
        for person in population:
            for area in person.town.area:
                if area.name == "Housing":
                    for x in area.houses:
                        x.transmission_chance *= 1  # Social distancing is not applied to housing
                elif area.name == "Work":
                    for x in area.work_spaces:
                        x.transmission_chance *= self.transmission_chance_reduction
                else:
                    area.transmission_chance *= self.transmission_chance_reduction

        return population


class Quarantine(Policy):
    def __init__(self, population_adherence_proportion=0.5):
        self.population_adherence_proportion = population_adherence_proportion
        super().__init__()

    def apply(self, population, time):
        number_of_people_who_will_quarantine = int(len(population) * self.population_adherence_proportion)

        indexes = list(range(len(population)))

        random.shuffle(indexes)

        indexes = indexes[:number_of_people_who_will_quarantine]

        for index, person in enumerate(population):
            if index in indexes:
                person.will_quarantine = True
            else:
                person.will_quarantine = False

        return population


class PolicyGroup:
    def __init__(self):
        self.policies = []
        self.active = True

    def add(self, policy, time):
        self.policies.append((time, policy))

    def get_current_policy(self, time):
        length, policy = self.policies.pop(0)

        if len(self.policies) == 0:
            self.active = False

        return policy, length


class EnglandSecondPolicy(Policy):
    def __init__(self):
        super().__init__()

    def apply(self, population, time):
        quarantine = Quarantine(population_adherence_proportion=0.8)
        work_from_home = WorkFromHome(["workspace_0", "workspace_1", "workspace_2"])
        reduce_shopping = ReduceShopping(0.5)
        delete_retirement_home_visiting_events = RemoveRetirementHomeVisitingEvents()
        remove_social_events = RemoveSocialEvents()
        reduce_school_events = ReduceSchoolAttendance(school_reduction=0.9)

        population = quarantine.apply(population, time)
        population = work_from_home.apply(population, time)
        population = reduce_shopping.apply(population, time)
        population = delete_retirement_home_visiting_events.apply(population, time)
        population = remove_social_events.apply(population, time)
        population = reduce_school_events.apply(population, time)

        return population


class SwedenFirstPolicy(Policy):
    def __init__(self):
        super().__init__()

    def apply(self, population, time):
        social_distancing = SocialDistancing(tranmission_chance_reduction=0.4)
        quarantine = Quarantine(population_adherence_proportion=0.65)
        reduce_school_events = ReduceSchoolAttendance(school_reduction=0.1)
        delete_retirement_home_visiting_events = RemoveRetirementHomeVisitingEvents()

        population = social_distancing.apply(population, time)
        population = quarantine.apply(population, time)
        population = reduce_school_events.apply(population, time)
        population = delete_retirement_home_visiting_events.apply(population, time)

        return population


def create_english_policy(first_policy_days, second_policy_days, third_policy_days):
    England = PolicyGroup()
    England.add(NoPolicy(), first_policy_days * 24 * 60 * 60)
    England.add(SocialDistancing(tranmission_chance_reduction=0.5), second_policy_days * 24 * 60 * 60)
    England.add(EnglandSecondPolicy(), third_policy_days * 24 * 60 * 60)

    return England


def create_swedish_policy(first_policy_days, second_policy_days):
    Sweden = PolicyGroup()
    Sweden.add(NoPolicy(), first_policy_days * 24 * 60 * 60)
    Sweden.add(SwedenFirstPolicy(), second_policy_days * 24 * 60 * 60)

    return Sweden
