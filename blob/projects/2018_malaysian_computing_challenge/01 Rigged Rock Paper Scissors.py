# © Philip Lee 2018 for MCC 2018

#games = input('Input array: ')
games = ["8< L", "O L", "8< D", "8< D", "8< W"]

i = 0
output = ''

while i < len(games):
    if games[i] == 'O W':
        output = output + '[],'
    elif games[i] == 'O L':
        output = output + '8<,'
    elif games[i] == 'O D':
        output = output + 'O,'
    elif games[i] == '[] W':
        output = output + '8<,'
    elif games[i] == '[] L':
        output = output + 'O,'
    elif games[i] == '[] D':
        output = output + '[],'
    elif games[i] == '8< W':
        output = output + 'O,'
    elif games[i] == '8< L':
        output = output + '[],'
    elif games[i] == '8< D':
        output = output + '8<,'
    else:
        print('error!')
    i += 1

print('Output: ' + output.rstrip(','))

print()
input('Press Enter to continue ...')
exit()
