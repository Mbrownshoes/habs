import urllib2
import json, re, csv
from bs4 import BeautifulSoup, Tag,SoupStrainer


# load the links to all teams pages
page = urllib2.urlopen("http://www.hockey-reference.com/teams/")
masterPage = BeautifulSoup(page)
table=masterPage.find("table")

rows = table.findAll('tr', {'class':'full_table'})

# loop through teams
for tr in rows:
    cols = tr.findAll('td')
    teamLink = cols[0].find('a').get('href')

    #PHX changed to ARI
    if teamLink == '/teams/PHX/':
        teamLink = '/teams/ARI/'

    # teamLink = '/teams/CBJ/'
    teamUrl="http://www.hockey-reference.com" + teamLink + "2015.html"
    
    # load each teams page
    teamPage = urllib2.urlopen(teamUrl)
    soup = BeautifulSoup(teamPage)

    # get team name
    title = soup.title

    if teamLink == '/teams/SJS/' or teamLink == '/teams/NJD/' or teamLink == '/teams/TBL/' or teamLink == '/teams/STL/' or teamLink == '/teams/LAK/':
        team_name=re.search(r'([ ])+([\w]+)([ ])([\w]+)',str(title))
        team_name =team_name.group(2) + " " +team_name.group(4)
    else:
        team_name=re.search(r'([ ])+([\w]+)',str(title)).group(2)

    if teamLink == '/teams/NYI/':
        team_name = 'NY Islanders'
    elif teamLink == '/teams/NYR/':
        team_name = 'NY Rangers'
    elif teamLink == '/teams/STL/':
        team_name = 'St. Louis'

    print(teamLink)

    players_table=soup.find("table", {'class' : 'sortable'})

    #find each player and get their url
    all = players_table.find_all("a", href=True)

    #create list of all players names

    # start building dict of each players assists
    master_list = {}
    players_list=[]

    # Load each player's page html
    for x in range (0, len(all)):
        url = all[x]['href']
        ind = re.search(r'/\w+/\w+/\w+', url).group()
        plyr_url = "http://www.hockey-reference.com" + ind + "/scoring/2015/"

        player_page = urllib2.urlopen(plyr_url)
        soup_plyr = BeautifulSoup(player_page)

        # Get players name
        player = soup_plyr.title.string
        player = (re.search(r'[^0-9]+ [^0-9]+', player)).group()

        # Get the stats table for player
        table=soup_plyr.find("table", {'class' : 'sortable'})

        goals=[]
        # if the player has no goals, skip
        if table:
            # Find goals a player got a point on
            for tr in table.findAll('tr'):
                if tr.findAll('a', href=True, text=teamLink[7:10]):
                   goals.append(tr.find_all("a", {'class' : 'highlight_text'}, re.compile(player))[0])    
            print(player)
            print(len(goals))

            # collect the name of players who assisted on his goals
            assists =[]
            for x in range(0,len(goals)):
                # print(player)
                # print(x)
                if goals[x].previousSibling == "Goal by ":
                    if goals[x].nextSibling == ", assisted by ":
                        assist1 =  goals[x].findNext('a')
                        assists.append(goals[x].findNext('a').text)
                       
                        if assist1.nextSibling == ' and ':
                            assists.append(assist1.findNext('a').text)

            #add players list to master dictionary
            master_list[player] = assists
        

    # json.dump(master_list, open(team_name + '_player_data.json', 'wb'))

    # create matrix

    ply=[]
    
    matrix = []

    assists = master_list
    players=assists.keys()
    # build list of assists for first player (Beaulieu)
    for i in range(0,len(assists)):

        # create new list for each player full of zeros    
        current = [0] * len(assists)

        #get players who assisted on Patches goals
        # print(players[i])


        x=assists[players[i]]
        print(x)
        for j in range(0, len(x)):  
            try:  
                ind=players.index(x[j]+' ')
                current[ind] += 1
            except:
                pass

        matrix.append(current)
    print(matrix)

    json.dump(matrix, open(team_name + '_matrix.json', 'wb'))

    with open(team_name + '_players.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["name","color"])
        for ind, val in enumerate(players):
            # save just the last names
            if val == 'Daniel Sedin ':
                val = 'D. Sedin '
            elif val == 'Henrik Sedin ':
                val = 'H. Sedin '    
            else:
                val = val.split(' ',1)[1]
            print(val.encode("utf-8"))
            writer.writerow([val.encode("utf-8"), ind])  

