# Household characteristics from the 2021 Census
# Source of data: https://www.ons.gov.uk/peoplepopulationandcommunity/householdcharacteristics/homeinternetandsocialmediausage/bulletins/householdandresidentcharacteristicsenglandandwales/census2021
# Office for National Statistics - Census 2021
# All data is rounded to the nearest 0.1%

DATA = {
    "one_person_aged_66_or_over": 12.9,
    "one_person_other": 17.3,
    "couple_family_no_children": 16.7,
    "couple_family_dependent_children": 18.8,
    "couple_family_all_nondependent_children": 6.4,
    "lone_parent_dependent_children": 6.9,
    "lone_parent_all_nondependent_children": 4.2,
    "other": 16.8,
}

# We will not consider the "other" category, so we will remove it from the data and scale up the other categories so the total is 100%
# This could lead to a possible error, as the other category is heavily biased towards one-person households (students).
# so our data will overrepresent families, however this is not a problem for our purposes as we are not simulating a university or college campus.

for key in DATA:
    DATA[key] *= 100 / (100 - DATA["other"])

del DATA["other"]

# Family households 2021 Dataset
# https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/families/datasets/familiesandhouseholdsfamiliesandhouseholds
# Office for National Statistics - Census 2021

# This data set is used to determine the number of children in a household
# The data is split into 3 categories: 0 children, 1 child, 2+ children
# As 0 children is already accounted for in the household data, we will only use the other two categories
# We will assume that single parent households have the same number of children as couple households as this is not covered in the data set

# Out of the 24510 family households with dependent children
# The number of households with 1-2 children is 19133
# The number of households with 3+ children is 5377

# We will assume that no households have more than 3 children
# We will also assume that the number of households with 1 child is the same as the number of households with 2 children
# This is not true, but it is a reasonable assumption for our purposes

# Breaking up the couple family households with dependent children into 1 child and 2+ children

DATA["couple_family_one_child"] = DATA["couple_family_dependent_children"] * (19133 / 2) / (19133 + 5377)
DATA["couple_famliy_two_children"] = DATA["couple_family_dependent_children"] * (19133 / 2) / (19133 + 5377)
DATA["couple_family_three_children"] = DATA["couple_family_dependent_children"] * 5377 / (19133 + 5377)

# Then the same for the lone parent

DATA["lone_parent_one_child"] = DATA["lone_parent_dependent_children"] * (19133 / 2) / (19133 + 5377)
DATA["lone_parent_two_children"] = DATA["lone_parent_dependent_children"] * (19133 / 2) / (19133 + 5377)
DATA["lone_parent_three_children"] = DATA["lone_parent_dependent_children"] * 5377 / (19133 + 5377)

# We will then assume that households with only non-dependent children only have 1 child

DATA["couple_family_one_nondependent_child"] = DATA["couple_family_all_nondependent_children"]
DATA["lone_parent_one_nondependent_child"] = DATA["lone_parent_all_nondependent_children"]


# Finally one_person_other will be simplified to one_person

DATA["one_person"] = DATA["one_person_other"]

# We will then remove the old categories
del (
    DATA["couple_family_dependent_children"],
    DATA["couple_family_all_nondependent_children"],
    DATA["lone_parent_dependent_children"],
    DATA["lone_parent_all_nondependent_children"],
    DATA["one_person_other"],
)

print(DATA)
