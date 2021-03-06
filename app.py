from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_cors import CORS, cross_origin

from datetime import datetime
import sqlite3
import sys

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

#SQL Tables

class UserAccount(db.Model):
    userID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200))
    fantasyTeam = db.Column(db.Integer, db.ForeignKey("esports_teams.teamID"))


class EsportsUser(db.Model):
    playerID = db.Column(db.Integer, primary_key = True)
    playerName = db.Column(db.String(200))
    teamID = db.Column(db.Integer, db.ForeignKey("esports_teams.teamID"))
    matches = db.relationship("EsportsMatchStats")

class EsportsTeams(db.Model):
    teamID = db.Column(db.Integer, primary_key = True)
    teamName = db.Column(db.String(200)) 
    gamesPlayed = db.Column(db.Integer)
    gamesWon = db.Column(db.Integer)

class EsportsMatch(db.Model):
    matchID = db.Column(db.Integer, primary_key = True)
    gameID = db.Column(db.Integer)
    matchType = db.Column(db.Integer)
    leagueName = db.Column(db.String(200))
    teamA = db.Column(db.String(200))
    teamB = db.Column(db.String(200))
    matchTime = db.Column(db.String(200))
    teamAWin = db.Column(db.Integer)
    teamBWin = db.Column(db.Integer)
    

class EsportsMatchStats(db.Model):
    matchID = db.Column(db.Integer, primary_key = True, unique=False)
    playerID = db.Column(db.Integer, db.ForeignKey("esports_user.playerID"), primary_key = True)
    matchType = db.Column(db.Integer, primary_key = True)
    leagueName = db.Column(db.String(200))
    playerName = db.Column(db.String(200))
    playerTeam = db.Column(db.Integer)
    legend = db.Column(db.String(200))
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    creepScore = db.Column(db.Integer)
    totalTeamKills = db.Column(db.Integer)
    matchTime = db.Column(db.String(200))
    killParticipation = db.Column(db.Integer)
    playerScore = db.Column(db.Integer)
    

    

class User(db.Model):
    playerID = db.Column(db.Integer, primary_key = True)
    playerName = db.Column(db.String(200))
    teamName = db.Column(db.String(200))
    matches = db.relationship("MatchStats")
    
class MatchStats(db.Model):
    matchID = db.Column(db.Integer, primary_key = True, unique=False)
    playerID = db.Column(db.Integer, db.ForeignKey("user.playerID"), primary_key = True)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    creepScore = db.Column(db.Integer)
    tripleKills = db.Column(db.Integer)
    quadKills = db.Column(db.Integer)
    pentaKills = db.Column(db.Integer)

    
#Routes

@app.route('/', methods=['GET'])
def index():
    allTeams = EsportsTeams.query.all()
    allMatches = EsportsMatch.query.all()
    lcsMatches = []
    lcsMatchStats = []
    lecMatches = []
    lecMatchStats = []
    lckMatches = []
    lckMatchStats = []
    lcsAcademyMatches = []
    lcsAcademyMatchStats = []
    allTeamPlayers = []
    allMatchesSorted = []
    allMatchStatsSorted = []
    sortedLCSMatches = []
    sortedLECMatches = []
    sortedLCKMatches = []
    sortedLCSAcademyMatches = []
    sortedLCSMatchStats = []
    sortedLECMatchStats = []
    sortedLCKMatchStats = []
    sortedLCSAcademyMatchStats = []

    runApp = True
    lastGameID = 0
    matchCount = len(allMatches)
    lcsData = []
    if(len(allMatches) > 0):
        lastGameID = int(allMatches[len(allMatches)-1].gameID)
    for matches in allMatches:
        if(str(matches.leagueName) == "LCS Academy"):
            lcsAcademyMatches.append(matches)
            lcsAcademyMatchStats.append(EsportsMatchStats.query.filter_by(matchID = matches.gameID).order_by(EsportsMatchStats.playerTeam).all())
        elif(str(matches.leagueName) == "LCS"):
            lcsMatches.append(matches)
            lcsMatchStats.append(EsportsMatchStats.query.filter_by(matchID = matches.gameID).order_by(EsportsMatchStats.playerTeam).all())
        elif(str(matches.leagueName) == "LEC"):
            lecMatches.append(matches)
            lecMatchStats.append(EsportsMatchStats.query.filter_by(matchID = matches.gameID).order_by(EsportsMatchStats.playerTeam).all())
        elif(str(matches.leagueName) == "LCK"):
            lckMatches.append(matches)
            lckMatchStats.append(EsportsMatchStats.query.filter_by(matchID = matches.gameID).order_by(EsportsMatchStats.playerTeam).all())
    if(len(allMatches) == 0):
        runApp = False

    previous = ""
    buildArray = []
    statsBuildArray = [] 
    innerBuildArray = []
    innerStatsBuildArray = []
    firstRun = True
    count = 0
    print(sortedLCSMatches, file=sys.stderr);
    for matches in lcsMatches:
        if(firstRun):
            innerBuildArray.append(matches)
            innerStatsBuildArray.append(lcsMatchStats[count])
            previous = matches.matchTime
            firstRun = False
        else:
            if(matches.matchTime != previous):
                buildArray.append(innerBuildArray)
                statsBuildArray.append(innerStatsBuildArray)
                innerStatsBuildArray = []
                innerBuildArray = []
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lcsMatchStats[count])
                previous = matches.matchTime
            else:
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lcsMatchStats[count])
        count += 1
    buildArray.append(innerBuildArray)
    statsBuildArray.append(innerStatsBuildArray)
    sortedLCSMatches = [buildArray, statsBuildArray]

    previous = ""
    buildArray = []
    statsBuildArray = []
    innerBuildArray = []
    innerStatsBuildArray = []
    firstRun = True
    count = 0
    for matches in lcsAcademyMatches:
        if(firstRun):
            innerBuildArray.append(matches)
            innerStatsBuildArray.append(lcsAcademyMatchStats[count])
            previous = matches.matchTime
            firstRun = False
        else:
            if(matches.matchTime != previous):
                buildArray.append(innerBuildArray)
                statsBuildArray.append(innerStatsBuildArray)
                innerStatsBuildArray = []
                innerBuildArray = []
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lcsAcademyMatchStats[count])
                previous = matches.matchTime
            else:
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lcsAcademyMatchStats[count])
        count += 1

    buildArray.append(innerBuildArray)
    statsBuildArray.append(innerStatsBuildArray)
    sortedLCSAcademyMatches = [buildArray, statsBuildArray]

    previous = ""
    buildArray = []
    statsBuildArray = [] 
    innerBuildArray = []
    innerStatsBuildArray = []
    firstRun = True
    count = 0
    for matches in lecMatches:
        if(firstRun):
            innerBuildArray.append(matches)
            innerStatsBuildArray.append(lecMatchStats[count])
            previous = matches.matchTime
            firstRun = False
        else:
            if(matches.matchTime != previous):
                buildArray.append(innerBuildArray)
                statsBuildArray.append(innerStatsBuildArray)
                innerStatsBuildArray = []
                innerBuildArray = []
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lecMatchStats[count])
                previous = matches.matchTime
            else:
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lecMatchStats[count])
        count += 1
    buildArray.append(innerBuildArray)
    statsBuildArray.append(innerStatsBuildArray)
    sortedLECMatches = [buildArray, statsBuildArray]

    previous = ""
    buildArray = []
    statsBuildArray = [] 
    innerBuildArray = []
    innerStatsBuildArray = []
    firstRun = True
    count = 0
    print(sortedLCSMatches, file=sys.stderr);
    for matches in lckMatches:
        if(firstRun):
            innerBuildArray.append(matches)
            innerStatsBuildArray.append(lckMatchStats[count])
            previous = matches.matchTime
            firstRun = False
        else:
            if(matches.matchTime != previous):
                buildArray.append(innerBuildArray)
                statsBuildArray.append(innerStatsBuildArray)
                innerStatsBuildArray = []
                innerBuildArray = []
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lckMatchStats[count])
                previous = matches.matchTime
            else:
                innerBuildArray.append(matches)
                innerStatsBuildArray.append(lckMatchStats[count])
        count += 1
    buildArray.append(innerBuildArray)
    statsBuildArray.append(innerStatsBuildArray)
    sortedLCKMatches = [buildArray, statsBuildArray]

    
    if(not runApp):
        sortedLCSMatches = []
        sortedLCSAcademyMatches = []
        sortedLCKMatches = []
        sortedLECMatches = []

    
    for team in allTeams:
        allTeamPlayers.append(EsportsUser.query.filter_by(teamID = team.teamID).all())


    return render_template('index.html', allTeams = allTeams, 
        allTeamPlayers=allTeamPlayers, allMatches = allMatches, 
        lastGameID = lastGameID, matchCount = matchCount, sortedLCSMatches = sortedLCSMatches, 
        sortedLCKMatches = sortedLCKMatches, sortedLECMatches = sortedLECMatches, 
        sortedLCSAcademyMatches = sortedLCSAcademyMatches, runApp = runApp, title="Show Teams")



@app.route('/updateDatabase', methods=['POST'])
def store_game_data():
    try:
        request_obj = request.get_json()

        if (EsportsTeams.query.filter_by(teamName = str(request.get_json()["teamName"])).first() == None):

            createEsportsTeam(str(request.get_json()["teamName"]))
        
        teamID = int(getEsportsTeam(request.get_json()["teamName"]).teamID)

        if (EsportsUser.query.filter_by(playerName = str(request.get_json()["playerName"])).first() == None):
            createEsportsUser(str(request.get_json()["playerName"]), teamID)

        user = getEsportsUser(request.get_json()["playerName"])
        updateTeamMatchWins(teamID, int(request.get_json()["matchWin"]))
        createEsportsMatch(int(request.get_json()["gameID"]), user.playerID, str(request.get_json()["playerName"]), str(request.get_json()["legend"]), int(request.get_json()["kills"]), int(request.get_json()["assists"]), int(request.get_json()["deaths"]), int(request.get_json()["creepScore"]), int(request.get_json()["teamTotal"]), int(request.get_json()["matchType"]), str(request.get_json()["matchTime"]), str(request.get_json()["teamA"]), str(request.get_json()["teamB"]), int(request.get_json()["teamAWin"]), int(request.get_json()["teamBWin"]), int(request.get_json()["playerTeam"]), str(request.get_json()["leagueName"]))        

        
        return ('', 204)
    except Exception as e:
        print(e)
        return ('', 500)



@app.route('/<matchID>/<playerName>/<kills>/<assists>/<deaths>/<creepScore>/<tripleKills>/<quadraKills>/<pentaKills>')
def indexAddPlayer(matchID, playerName, kills, assists, deaths, creepScore, tripleKills, quadraKills, pentaKills):
    addUser(playerName)
    addMatchStats(int(matchID), int(getUserID(playerName)), int(kills), int(assists), int(deaths), int(creepScore), int(tripleKills), int(quadraKills), int(pentaKills))
    return render_template('index.html')


#SQL Helper Functions

def updateTeamMatchWins(teamID, matchWin):
    team = EsportsTeams.query.filter_by(teamID=teamID).first()
    gamesplayed = int(team.gamesPlayed)
    gamesplayed += 1
    gameswon = int(team.gamesWon)
    if(matchWin == 1):
        gameswon += 1 
    team.gamesPlayed = gamesplayed
    team.gamesWon = gameswon
    db.session.commit()


def getEsportsMatch(gameID):
    matches = EsportsMatchStats.query.filter_by(gameID = gameID).all()

def createEsportsMatch(gameID, playerID, playerName, legend, kills, assists, deaths, creepScore, totalTeamKills, matchType, matchTime, teamA, teamB, teamAWin, teamBWin, playerTeam, leagueName):
    matchStats = EsportsMatchStats(matchID = gameID, playerName = playerName, playerID = playerID, legend = legend, kills = kills, assists = assists, deaths = deaths, creepScore = creepScore, totalTeamKills = totalTeamKills, matchType = matchType, leagueName = leagueName, matchTime = matchTime, playerTeam = playerTeam, killParticipation = (totalTeamKills / max(1, kills+assists)), playerScore = calculatePlayerScore(kills, assists, deaths, creepScore, totalTeamKills))
    if (EsportsMatch.query.filter_by(gameID = gameID).first() == None):
        match = EsportsMatch(gameID = gameID, teamA = teamA, teamB = teamB, matchTime = matchTime, teamAWin = teamAWin, teamBWin = teamBWin, matchType = matchType, leagueName = leagueName)
        db.session.add(match)

    db.session.add(matchStats)
    db.session.commit()

def getEsportsTeam(teamName):
    team = EsportsTeams.query.filter_by(teamName=teamName).first()
    return team

def createEsportsTeam(teamName):
    team = EsportsTeams(teamName = teamName, gamesPlayed = 0, gamesWon = 0)
    db.session.add(team)
    db.session.commit()

def createEsportsUser(playerName, teamID):
    user = EsportsUser(playerName=playerName, teamID=teamID)
    db.session.add(user)
    db.session.commit()

def getEsportsUser(playerName):
    user = EsportsUser.query.filter_by(playerName=playerName).first()
    return user

def addEsportUser(playerName):
    user = EsportsUser(playerName = playerName)
    db.session.add(user)
    db.session.commit()

def addUser(playerName):
    user = User(playerName = playerName)
    db.session.add(user)
    db.session.commit()



def getUserID(playerName):
    user = User.query.filter_by(playerName=playerName).first()
    return user.playerID

def addMatchStats(matchID, playerID, kills, assists, deaths, creepScore, tripleKills, quadraKills, pentaKills):
    match = MatchStats(matchID = matchID, playerID = playerID, kills = kills, assists = assists, deaths = deaths, creepScore = creepScore, tripleKills = tripleKills, quadKills = quadraKills, pentaKills = pentaKills)
    db.session.add(match)
    db.session.commit()

def calculatePlayerScore(kills, assists, deaths, creepScore, teamTotalKills):
        flawless = 1
        if(deaths == 0):
            flawless = 1.2
        killPoints = kills*3
        assistsPoints = assists*2
        deathsPoints = deaths*0.5
        creepScorePoints = creepScore*0.02
        killAssistBonus = int((kills + assists) / 10)*2
        participation = ((kills + assists) / max([1, teamTotalKills]))*100
        participation *= 0.25
        playerScore = killPoints + assistsPoints + creepScorePoints + killAssistBonus + participation - deathsPoints
        playerScore *= flawless 
        return round(playerScore, 2)
    
if __name__ == "__main__":
    app.run(debug=True)
