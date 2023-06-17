# © Philip Lee 2018 for MCC 2018

import math

K = int(input('Input your value of K: '))

print()
print('For K = ' + str(K) + ',')


power2 = int(math.ceil(math.log(K,2)))
print('Nearest 2^n power after K: 2^' + str(power2) + ' (' + str(2 ** power2) + ')')

diffbase10 = (2 ** power2) - K
print('Difference in decimal: ' + str(diffbase10))

diffbase2 = str(bin(diffbase10)).replace('0b','')
print('Difference in binary: ' + str(diffbase2))

sumofdigits = diffbase2.count('1')
print('Sum of binary digits: ' + str(sumofdigits))

print()
input('Press Enter to continue ...')
exit()
