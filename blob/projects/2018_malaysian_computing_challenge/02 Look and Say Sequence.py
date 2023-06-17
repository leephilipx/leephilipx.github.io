# © Philip Lee 2018 for MCC 2018

#sequence = input('Input a sequence: ')
sequence = "4444444766666333881118888888"

split_sequence = list(str(sequence))
i = 0
split_index = 0
groupNumbers = ''
grouped = []
x = 0
output = ''

while i < len(split_sequence):
    if split_sequence[i] != split_sequence[i-1]:
        while split_index < i:
            groupNumbers = groupNumbers + split_sequence[split_index]
            split_index += 1
        grouped.append(groupNumbers)
        groupNumbers = ''
    i += 1
    
while split_index < len(split_sequence):
    groupNumbers = groupNumbers + split_sequence[split_index]
    split_index += 1
grouped.append(groupNumbers)

if grouped[0] == '': # Weird error if input one digit only
    grouped.remove('')

print('Grouped by numbers: ' + str(grouped))

while x < len(grouped):
    output = output + str(len(grouped[x])) + str(grouped[x])[0]
    x += 1

print('Output: ' + output)

print()
input('Press Enter to continue ...')
exit()
