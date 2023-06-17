# © Philip Lee 2018 for MCC 2018

#k = input('Input your array: ')
k = [6, 3, 2]

i = 1
ID = []
step = 0
index = 0

while i <= len(k)+1:
    ID.append(str(i))
    i += 1

while step < len(k):
    index += k[step]-1
    index = index % len(ID)
    del ID[index]
    step += 1

print('ID of last person: ' + str(ID[0]))

print()
input('Press Enter to continue ...')
exit()
