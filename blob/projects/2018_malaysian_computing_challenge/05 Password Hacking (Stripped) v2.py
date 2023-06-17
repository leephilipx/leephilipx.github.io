# © Philip Lee 2018 for MCC 2018

import math
import itertools

#unknown_sum = int(input('Input the number of unknown values: '))
unknown_sum = 12

# 59279 '?' for case 7

unknown_notspecified = unknown_sum - 9
unknown_combinations = list(itertools.combinations_with_replacement('LUN', 9))

combinations = 0
i = 0

while i < len(unknown_combinations):
    L_count = unknown_combinations[i].count('L')
    U_count = unknown_combinations[i].count('U')
    N_count = unknown_combinations[i].count('N')
    combinations = (combinations + ((62 ** unknown_notspecified) * (26 ** L_count) * (26 ** U_count) * (10 ** N_count)
                                    * (unknown_sum*(unknown_sum-1)*(unknown_sum-2)*(unknown_sum-3)*(unknown_sum-4)
                                       *(unknown_sum-5)*(unknown_sum-6)*(unknown_sum-7)*(unknown_sum-8))
                                    / math.factorial(L_count) / math.factorial(U_count) / math.factorial(N_count)))
    print(str(unknown_combinations[i]) + ", " + str(i) + ": " + str(int(combinations)))
    i += 1

combinations = ((62 ** unknown_sum) - combinations) % 1000000007

print('Combinations: ' + str(int(combinations)))

print()
input('Press Enter to continue ...')
exit()

