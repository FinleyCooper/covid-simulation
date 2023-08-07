# fmt: off
DATA = [1.0, 1.1, 1.1, 1.1, 1.1, 1.2, 1.1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.1, 1.1, 1.1, 1.1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.2, 1.2, 1.2, 1.2, 1.3, 1.3, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.3, 1.3, 1.2, 1.2, 1.2, 1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9, 1.0, 1.0, 1.1, 1.0, 0.8, 0.8, 0.7, 0.7, 0.6, 0.5, 0.6, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0]
# fmt: on


def distribute_ages(population_size):
    # The population is distributed according to the percentages in DATA
    ages = []

    for age, percentage in enumerate(DATA):
        ages.extend([age] * round(population_size * percentage / 100))

    # Add the remainder to the modal age
    ages.extend([DATA.index(max(DATA))] * (population_size - len(ages)))

    return sorted(ages)
