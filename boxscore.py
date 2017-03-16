import nba
from collections import OrderedDict
from player import *
import pprint

mapping = OrderedDict([
            ("Player","player"),
            ("Min","min"),
            ("FG",["fga", "fgm"]),
            ("3PT",["tpa", "tpm"]),
            ("FT",["fta", "ftm"]),
            ("OReb","offReb"),
            ("DReb","defReb"),
            ("Reb","totReb"),
            ("Ast","assists"),
            ("Stl","steals"),
            ("Blk","blocks"),
            ("TO","turnovers"),
            ("PF","pFouls"),
            ("+/-","plusMinus"),
            ("Pts","points") ])


def parse_quarter_to_table(team):
    content = "<th>" + team['team'] + "</th>"
    total = 0
    for quarter in team['quarters']:
        total += int(quarter)
        content += "<td>" + quarter + "</td>"
    content += "<td>" + str(total) + "</td>"
    return content

def generate_summary_table(home, away):
    nth = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "OT1", 6: "OT2", 7: "OT3"}
    table = "<center><table><tr><th/>"
    for i in range(0, len(home['quarters'])):
        table += "<th>" + nth[i+1] + "</th>"
    table += "<th>Total</th>"
    table += "<tr>" + parse_quarter_to_table(home) + "</tr>"
    table += "<tr>" + parse_quarter_to_table(away) + "</tr>"
    table += "</table></center>"
    return table

def parse_boxscore(team, boxscore):
    stats = boxscore.get('stats')
    table = "<h2>" + team['team'] + "</h2>"
    count = 0
    for player in stats.get('activePlayers'):
        if team.get('teamId') == player.get('teamId'):
           p = Player(**player)
           count += 1
           if count == 6:
               table += "<tr><th colspan=15><center>Bench</center></th></tr>"
           table += "<tr>"
           for key, value in mapping.items():
               if key == "Player":
                   table += "<th>" + getattr(p,value) + "</th>"
               else:
                   if isinstance(value, list):
                       table += "<td>" + str(getattr(p,value[1])) + "-" + str(getattr(p,value[0])) + "</td>"
                   else:
                       table += "<td>" + str(getattr(p,value)) + "</td>"
           table += "</tr>"
    return table

def generate_boxscore(team_id, boxscore):
    table = "<div class='datagrid'><table>"
    table += "<tr><th colspan=15><center>Starters</center></th></tr>"
    for head in mapping.keys():
        table += "<th>" + head + "</th>"
    table += "</tr>"
    table += parse_boxscore(team_id, boxscore)
    table += "</div></table>"
    return table
