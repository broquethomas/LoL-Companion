from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import sys
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

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


class EsportsMatchStats(db.Model):
    matchID = db.Column(db.Integer, primary_key = True, unique=False)
    playerID = db.Column(db.Integer, db.ForeignKey("esports_user.playerID"), primary_key = True)
    matchType = db.Column(db.Integer, primary_key = True)
    legend = db.Column(db.String(200))
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    creepScore = db.Column(db.Integer)
    totalTeamKills = db.Column(db.Integer)
    

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

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<matchID>/<playerName>/<kills>/<assists>/<deaths>/<creepScore>/<tripleKills>/<quadraKills>/<pentaKills>')
def indexAddPlayer(matchID, playerName, kills, assists, deaths, creepScore, tripleKills, quadraKills, pentaKills):
    addUser(playerName)
    addMatchStats(int(matchID), int(getUserID(playerName)), int(kills), int(assists), int(deaths), int(creepScore), int(tripleKills), int(quadraKills), int(pentaKills))
    return render_template('index.html')

@app.route('/<gameID>/<playerName>/<teamName>/<matchWin>/<legend>/<kills>/<assists>/<deaths>/<creepScore>/<teamTotal>/<matchType>')
def indexAddEsportPlayer(gameID, playerName, teamName, matchWin, legend, kills, assists, deaths, creepScore, teamTotal, matchType):
    if (EsportsTeams.query.filter_by(teamName = teamName).first() == None):
        createEsportsTeam(str(teamName))
    
    teamID = int(getEsportsTeam(teamName).teamID)
    
    if (EsportsUser.query.filter_by(playerName = playerName).first() == None):
        createEsportsUser(str(playerName), teamID)

    user = getEsportsUser(playerName)
    print(playerName, file=sys.stderr)
    updateTeamMatchWins(teamID, int(matchWin))
    createEsportsMatch(int(gameID), user.playerID, str(legend), int(kills), int(assists), int(deaths), int(creepScore), int(teamTotal), int(matchType))        
    return render_template('index.html')

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

def createEsportsMatch(gameID, playerID, legend, kills, assists, deaths, creepScore, totalTeamKills, matchType):
    match = EsportsMatchStats(matchID = gameID, playerID = playerID, legend = legend, kills = kills, assists = assists, deaths = deaths, creepScore = creepScore, totalTeamKills = totalTeamKills, matchType = matchType)
    db.session.add(match)
    db.session.commit()

def getEsportsTeam(teamName):
    team = EsportsTeams.query.filter_by(teamName=teamName).first()
    print(team, file=sys.stderr)
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
    print("HERHEHEREHREH", file=sys.stderr)
    print(user, file=sys.stderr)
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

def calculatePlayerScore(kills, assists, deaths, creepScore, tripleKills, quadraKills, pentaKills):
        flawless = 0
        if(deaths == 0):
            flawless = 5
        
        killAssistBonus = int((kills + assists) / 10)
        playerScore = (kills*3 + assists*2) + creepScore*0.02 + killAssistBonus + tripleKills*2 + quadraKills*5 + pentaKills*10 - deaths*0.5
        return playerScore
    
if __name__ == "__main__":
    app.run(debug=True)