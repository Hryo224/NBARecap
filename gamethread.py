import praw
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
PASSWORD = os.environ.get("REDDIT_USER_PWD")
USER_AGENT = os.environ.get("REDDIT_USER_AGENT")
USER_NAME = os.environ.get("REDDIT_USER_NAME")

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        password=PASSWORD, user_agent=USER_AGENT, username=USER_NAME)

def get_game_thread(date, game):
    comment_arr = []
    threads = reddit.subreddit("nba").hot(limit = 250)
    for thread in threads:
        title = thread.title
        if "GAME THREAD" in title and date in title and game in title:
            print(game)
            thread.comments.replace_more(limit=0)
            comment_queue = thread.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                comment_arr.append(comment.body)
                comment_queue.extend(comment.replies)
    return comment_arr

def generate_wordcloud(date, game):
    gamethread = get_game_thread(date, game)
    words = ' '.join([str(x) for x in gamethread])
    wordcloud = WordCloud().generate(words)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("images/" + game.replace(" ",'') + date.replace(" ", '') + ".png")
