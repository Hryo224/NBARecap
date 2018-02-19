import boxscore as b
import pdfkit as p
from NBAData import nba_data
import pprint
import os
from datetime import datetime, date, timedelta

def generate_report(boxscore, home, away, article, date, city):
    content = "<html><head><link rel='stylesheet' type='text/css' href='" + os.environ.get("CSS_LOC") + "'>"
    content += "<center><h1>" + home.get('team') + " vs " + away.get('team') + "</h1></center>"
    content += b.generate_summary_table(home, away)
    content += b.generate_boxscore(home, boxscore)
    content += b.generate_boxscore(away, boxscore)
    content += article
    content += "</html>"
    return content

def get_scoreboard(date):
    scoreboard = nba_data("scoreboard", date)
    return scoreboard

def get_article(game, date):
    game_id = game.get('gameId')
    recap = nba_data("recap_article", date, game_id)
    recap_paras = recap.get('paragraphs')
    article = "<center><h2> AP Summary </h2></center>"
    for paragraph in recap_paras:
        article += "<p>" + paragraph.get('paragraph') + "</p>"
    return article

def get_game_data(game, team):
    game_data = {}
    quarter_data = []
    team_data = game.get(team)
    per_quarter = team_data.get('linescore')
    for quarter in per_quarter:
        quarter_data.append(quarter.get('score'))
    game_data['quarters'] = quarter_data
    game_data['team'] = team_data.get('triCode')
    game_data['teamId'] = team_data.get('teamId')
    game_data['duration'] = team_data.get('gameDuration')
    game_data['attendance'] = team_data.get('attendance')
    return game_data

def init(date):
    formatted_date = datetime.strptime(date, '%Y%m%d').strftime('%B %d, %Y')
    dir = "html/"+date+"/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    for game in get_scoreboard(date).get('games'):
        boxscore = nba_data("boxscore", date, game.get('gameId'))
        home = get_game_data(game, 'hTeam')
        away = get_game_data(game, 'vTeam')
        article = get_article(game, date)
        city = find_team_city(home.get('team'))
        report = generate_report(boxscore, home, away, article, formatted_date, city)
        file_name = home.get('team') + "vs" + away.get('team') + date + ".pdf"
        p.from_string(report, file_name)
        os.rename(file_name, dir+file_name)
        
def get_yesterday_date():
    return (date.today() - timedelta(1)).strftime('%Y%m%d')

def find_team_city(triCode):
    teams = nba_data("teams", 2017).get('league').get('standard')
    for team in teams:
        if team.get('tricode') == triCode:
            return team.get('city')

if __name__ == "__main__":
    calendar = nba_data("calendar")
    date = get_yesterday_date()
    if date in calendar:
        init(date)    
