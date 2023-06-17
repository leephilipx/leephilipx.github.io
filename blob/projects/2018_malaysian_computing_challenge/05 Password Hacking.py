# © Philip Lee 2018 for MCC 2018

import math
import itertools

#password = str(input('Input your known password string: '))
password = "?????????????????????"

# 59279 '?' for case 7

# Total lowercase characters
lowercase_sum = 0
for lowercase in 'abcdefghijklmnopqrstuvwxyz':
    lowercase_sum = lowercase_sum + password.count(lowercase)
print('Total lowercase characters: ' + str(lowercase_sum))

# Total uppercase characters
uppercase_sum = 0
for uppercase in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    uppercase_sum = uppercase_sum + password.count(uppercase)
print('Total uppercase characters: ' + str(uppercase_sum))

# Total numerical characters
numerical_sum = 0
for numerical in '0123456789':
    numerical_sum = numerical_sum + password.count(numerical)
print('Total numerical characters: ' + str(numerical_sum))

# Total '?' characters
unknown_sum = password.count('?')
print('Total unknown characters: ' + str(unknown_sum))

# How many more mandatory characters?
lowercase_diff = 0
uppercase_diff = 0
numerical_diff = 0

if lowercase_sum < 3:
    lowercase_diff = 3 - lowercase_sum
if uppercase_sum < 3:
    uppercase_diff = 3 - uppercase_sum
if numerical_sum < 3:
    numerical_diff = 3 - numerical_sum

unknown_notspecified = unknown_sum - lowercase_diff - uppercase_diff - numerical_diff
unknown_combinations = list(itertools.combinations_with_replacement('LUN', unknown_notspecified))

combinations = 0
i = 0

while i < len(unknown_combinations):
    L_count = unknown_combinations[i].count('L') + lowercase_diff
    U_count = unknown_combinations[i].count('U') + uppercase_diff
    N_count = unknown_combinations[i].count('N') + numerical_diff
    combinations = (combinations + ((26 ** L_count) * (26 ** U_count) * (10 ** N_count) * math.factorial(unknown_sum) / math.factorial(L_count) / math.factorial(U_count) / math.factorial(N_count))) % 1000000007
    i += 1

print('Combinations: ' + str(int(combinations)) + ' (mod 1000000007)')

print()
input('Press Enter to continue ...')
exit()
