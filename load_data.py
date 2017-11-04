import urllib.request
import json, re, csv
from bs4 import BeautifulSoup, Tag,SoupStrainer


# load the links to all teams pages
page = urllib.request.urlopen("http://www.hockey-reference.com/teams/")
masterPage = BeautifulSoup(page)
table=masterPage.find("table")

rows = table.findAll('tr', {'class':'full_table'})
season = '2018'
# loop through teams
 
for tr in rows:
#    print "TR: "
    # print(type(tr))
    try:
        teamLink = tr.find('a').get('href')
    #    teamLink = cols[0].find('a').get('href')
    
        #PHX changed to ARI
        if teamLink == '/teams/PHX/':
            teamLink = '/teams/ARI/'
    
        # teamLink = '/teams/CBJ/'
        teamUrl="http://www.hockey-reference.com" + teamLink + season+ ".html"
    
        # load each teams page
        teamPage = urllib.request.urlopen(teamUrl)
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
    
    #    players_table=soup.find("table", {'class' : 'sortable stats_table'})
        players_table=soup.find("div", {'id' : 'div_skaters'})
        #find each player and get their url
        all = players_table.find_all("a", href=True)
    
        #create list of all players names
    
        # start building dict of each players assists
        master_list = {}
        points_list ={}
     
    
        # Load each player's page html
        for x in range (0, len(all)):
            url = all[x]['href']
            ind = re.search(r'/\w+/\w+/\w+', url).group()
            plyr_url = "http://www.hockey-reference.com" + ind + "/scoring/"+season
    
            player_page = urllib.request.urlopen(plyr_url)
            soup_plyr = BeautifulSoup(player_page, 'html5lib')
    
            # Get players name
            player = soup_plyr.title.string
            print(player)
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
                # print(player)
    #            print(len(goals))  
                # collect the name of players who assisted on his goals
                assists =[]
                points_season = len(goals)
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
                points_list[player] = points_season
            
    
        json.dump(master_list, open(team_name + '_player_data.json', 'w')) #goal scorer:[players who assisted on his goals]
    
        # create matrix
    
        ply=[]
        
        matrix = []
    
        assists = master_list
        players=list(assists)
        # build list of assists for first player (Beaulieu)
        for i in range(0,len(assists)):
    
            # create new list for each player full of zeros. list is lenghth of all players that have at least 1 point    
            current = [0] * len(assists)
    
            #get players who assisted on Patches goals
            #print(players[i])
    
    
            x=assists[players[i]]
            # print(x)
            for j in range(0, len(x)):  
                try:  
                    ind=players.index(x[j]+' ') #the player with the assists position in the team index
                    current[ind] += 1
                except:
                    pass
    
            matrix.append(current)
    
        json.dump(matrix, open(team_name + '_matrix'+season+'.json', 'w'))
    
        with open(team_name + '_players'+season+'.csv', "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(["name","points"])
            for ind, val in enumerate(players):
                # save just the last names
                if val == 'Daniel Sedin ':
                    val = 'D. Sedin '
                elif val == 'Henrik Sedin ':
                    val = 'H. Sedin '    
                else:
                    val1 = val.split(' ',1)[1]
                writer.writerow([val1, points_list[val]])  
    except:
        print(tr)
