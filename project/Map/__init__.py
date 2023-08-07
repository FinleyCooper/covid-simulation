from Map import GroupedTransmissionAreas, TransmissionAreas, clock
from Map.constants import positions, SIMULATION_SPEED


def none_function(*args, **kwargs):
    return None


class AreaList:
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield value


class Town:
    def __init__(self, calc_R0=False, on_infection=none_function, on_recovery=none_function):
        self.quarantined_households = set()
        self.area = AreaList()
        self.clock = clock.Clock(simulation_speed=SIMULATION_SPEED)
        self.calc_R0 = calc_R0
        self.on_infection = on_infection
        self.on_recovery = on_recovery


def create_map(calc_R0=False, on_infection=none_function, on_recovery=none_function):
    town = Town(calc_R0=calc_R0, on_infection=on_infection, on_recovery=on_recovery)

    town.area.housing = GroupedTransmissionAreas.Housing()
    town.area.work = GroupedTransmissionAreas.Work()

    town.area.school = TransmissionAreas.School(name="School", width=5, height=3)
    town.area.retirement_home = TransmissionAreas.RetirementHome(name="Retirement Home", width=2.5, height=1.4)
    town.area.shops = TransmissionAreas.CommunityArea(name="Shops", width=2.5, height=1.4)
    town.area.theatre = TransmissionAreas.SocialArea(name="Theatre", width=1.4, height=1.4)
    town.area.sports_centre = TransmissionAreas.CommunityArea(name="Sports Centre", width=2.5, height=1.4)
    town.area.bar = TransmissionAreas.SocialArea(name="Bar", width=1.4, height=1.4)
    town.area.restaurant = TransmissionAreas.SocialArea(name="Restaurant", width=1.4, height=1.4)
    town.area.club = TransmissionAreas.SocialArea(name="Club", width=1.4, height=1.4)

    town.area.retirement_home.move_to(positions.retirement_home)
    town.area.school.move_to(positions.school)
    town.area.housing.move_to(positions.housing)
    town.area.work.move_to(positions.work)
    town.area.club.move_to(positions.club)
    town.area.bar.move_to(positions.bar)
    town.area.restaurant.move_to(positions.restaurant)
    town.area.theatre.move_to(positions.theatre)
    town.area.sports_centre.move_to(positions.sports_centre)
    town.area.shops.move_to(positions.shops)

    town.clock.move_to(positions.clock)

    return town
