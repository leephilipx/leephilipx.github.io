# © Philip Lee 2018 for MCC 2018

import math
import itertools

unknown_sum = int(input('Input the number of unknown values: '))
#unknown_sum = 9

# 59279 '?' for case 7

lowercase_diff = 3
uppercase_diff = 3
numerical_diff = 3

unknown_notspecified = unknown_sum - lowercase_diff - uppercase_diff - numerical_diff
unknown_combinations = list(itertools.combinations_with_replacement('LUN', unknown_notspecified))

combinations = 0
i = 0

while i < len(unknown_combinations):
    L_count = unknown_combinations[i].count('L') + lowercase_diff
    U_count = unknown_combinations[i].count('U') + uppercase_diff
    N_count = unknown_combinations[i].count('N') + numerical_diff
    combinations = (combinations + ((26 ** L_count) * (26 ** U_count) * (10 ** N_count) * math.factorial(unknown_sum) / math.factorial(L_count) / math.factorial(U_count) / math.factorial(N_count))) % 1000000007
    print(str(unknown_combinations[i]) + ", " + str(i) + ": " + str(int(combinations)))
    i += 1

print('Combinations: ' + str(int(combinations)))

print()
input('Press Enter to continue ...')
exit()
