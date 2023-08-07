# Results from data_analysis/census/households.py (Appendix 1)
DATA = {
    "one_person_aged_66_or_over": 15.504807692307692,
    "couple_family_no_children": 20.072115384615383,
    "couple_family_one_child": 8.819506559332142,
    "couple_famliy_two_children": 8.819506559332142,
    "couple_family_three_children": 4.9571407274895645,
    "lone_parent_one_child": 3.2369465563506266,
    "lone_parent_two_children": 3.2369465563506266,
    "lone_parent_three_children": 1.8193761180679786,
    "couple_family_one_nondependent_child": 7.6923076923076925,
    "lone_parent_one_nondependent_child": 5.048076923076923,
    "one_person": 20.79326923076923,
}


def distribute_households(number_of_households):
    # Distribute the 70 houses across the 7 categories by the value given in DATA
    housesholds = {}

    for key in DATA:
        housesholds[key] = int(DATA[key] / 100 * number_of_households)

    # Add the remainder to the category with the highest percentage
    housesholds[max(housesholds, key=housesholds.get)] += number_of_households - sum(housesholds.values())

    # check if the sum of the values is equal to NUMBER_OF_HOUSEHOLDS
    assert sum(housesholds.values()) == number_of_households

    return housesholds
