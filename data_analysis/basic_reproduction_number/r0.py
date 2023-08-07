import numpy as np
import scipy.stats as st

# Get the confidence interval of a list of numbers which will be our simulation R0
get_confidence_interval = lambda a: st.t.interval(0.95, len(a) - 1, loc=np.mean(a), scale=st.sem(a))


DATA = [
    2.493827160493827,
    2.7222222222222223,
    2.765432098765432,
    2.54320987654321,
    2.5246913580246915,
    2.549382716049383,
    2.7037037037037037,
    2.6481481481481484,
    2.6790123456790123,
    2.6481481481481484,
]

lower, upper = get_confidence_interval(DATA)
mean = np.mean(DATA)

# Print the results
print(f"The average number for R0 is {round(mean, 2)} (95% CI: {round(lower, 2)}-{round(upper, 2)})")
