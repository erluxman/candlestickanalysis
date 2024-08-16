import numpy as np
from scipy.stats import f_oneway

np.random.seed(0)  # For reproducibility
group1 = np.random.normal(loc=5.0, scale=1.0, size=30)
group2 = np.random.normal(loc=6.0, scale=1.0, size=30)
group3 = np.random.normal(loc=7.0, scale=1.0, size=30)


# Method to perform ANOVA test
def calculate_anova(data1, data2, data3):
    F_statistic, p_value = f_oneway(data1, data2, data3)
    return F_statistic, p_value


# Calculate ANOVA
anova_result = calculate_anova(group1, group2, group3)
print(
    "ANOVA Test Result: F-statistic =", anova_result[0], ", p-value =", anova_result[1]
)
