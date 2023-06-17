# © Philip Lee 2018 for MCC 2018

# Answer for case 6 by moving the letter forward one by one
i = 0
end = 41644-1
combinations = 0
while i <= end:
    combinations = (combinations + (26 * (36 ** i) * (62 ** (end-i)))) % 1000000007
    print(str(i)+ ': ' + str(combinations))
    i += 1
print(combinations)
