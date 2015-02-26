import json, csv, re

with open("player_data.json") as assists:
    assists = json.load(assists)

ply=[]
    
matrix = []

players=assists.keys()
# build list of assists for first player (Beaulieu)
for i in range(0,len(assists)):

    # create new list for each player full of zeros    
    current = [0] * len(assists)

    #get players who assisted on Patches goals
    print(players[i])


    x=assists[players[i]]
    for j in range(0, len(x)):    
        ind=players.index(x[j]+' ')
        current[ind] += 1

    matrix.append(current)
print(matrix)

json.dump(matrix, open('matrix.json', 'wb'))

csvfile='players.csv'
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["name","color"])
    for ind, val in enumerate(players):
        # save just the last names
        val = val.split()[1]
        writer.writerow([val, ind])  