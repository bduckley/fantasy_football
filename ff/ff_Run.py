from ff_espn_api import League
import matplotlib.pyplot as plt
import numpy as np

league_id = 692156
year = 2018
espn_s2 = 'AEBlxO7SfF6cuPjEvujvAbpQ5fmvr7oYPxIyQV9qsazYKOuNCN14sb%2FBGr4yOyXwUtLTS8a4igLp2SrraMI6lC1EoWiHHKPhUZyqMiS%2B7JCKSapXyDbqHnX8ur1Ga0q3d7sGe9i4gi8ZKbIqaZWhJBdEqqa2UXBDLrgoxpUade%2BzepUwahpfqOvzOr87TiXACwdcnRIqPmhXGW4SuPU8kMlLqWPgj3zL%2FGLKF%2B%2B2gZ1AQxgHUBXYIXpHatVRgWndZNPLIfehi8FV5Xmi8PZnWP2%2F'
swid = "{E9BFC86F-E2A7-4FD8-BFC8-6FE2A71FD8B5}"
league = League(league_id, year, espn_s2, swid)
#league = League(league_id,year)
[teamDave, teamLuke, teamFef, teamCody, teamAddy, teamJoel, teamEric, teamTanner, teamTracy, teamBrittain] = league.teams
labels = ('Dave','Luke','Fef','Cody','Addy','Joel','Eric', 'Tanner', 'Tracy','Brittain')

#grab head2head wins
winsH2H = np.zeros(shape = (10,1))
i = 0
for teamName in league.teams:
    winsH2H[i]=teamName.wins
    i += 1
winsH2H = np.transpose(winsH2H)[0]

def playEveryone(teamNames):
    weeklyScores = np.zeros(shape=(10,14))
    j = 0
    for teamName in teamNames: # for each team
        weeklyScores[j] = teamName.scores
        j += 1
    wins = np.zeros(shape=(1,10))
    for i in range(14):
        wins += (weeklyScores[:,i] > np.median(weeklyScores[:,i]))
    
##    return weeklyScores
    wins = wins[0]
##    return wins

    plt.subplot(1,3,1)
    plt.bar(range(10),winsH2H)
    plt.xticks(range(10),labels,rotation='vertical')
    plt.title('head2head wins')

##    plt.subplot(1,3,1)
##    plt.bar(range(10),wins*(1/2) + winsH2H*(1/2))
##    plt.xticks(range(10),labels,rotation='vertical')
##    plt.title('scoring: 3/4 pts H2H; 1/4 pts Median')

    plt.subplot(1,3,3)
    plt.bar(range(10),wins*(1/4) + winsH2H*(3/4))
    plt.xticks(range(10),labels,rotation='vertical')
    plt.title('scoring: 3/4 pts H2H; 1/4 pts Median')

##    adjustedScore = winsH2H*(2/3)+wins*(1/3)
    plt.subplot(1,3,2)
    plt.bar(range(10),wins*(1/3) + winsH2H*(2/3))
    plt.xticks(range(10),labels,rotation='vertical')
    plt.title('scoring: 2/3 pts H2H; 1/3 pts Median')
            
        
def plotWeeklyScores(teamNames):
    legendList = []
    for teamName in teamNames:
        plt.plot(range(14), teamName.scores, marker = 'o')
        legendList = legendList + [str(teamName)]
    plt.xlabel('Week #')
    plt.ylabel('Weekly Scores')
    plt.legend(legendList)



listTeams = [str(team) for team in league.teams]

