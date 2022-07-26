# Twitter bot for Llamafax service
from lib.tweetlib import startUp
import random
import tweepy
from lib.MongoDB import MongoDB
import logging
from time import sleep
import os


# [VARS]
ReadOnly = False
WaitInt = int(os.getenv("WAIT", 6))
CharacterLimit = 280

LogLevel = logging.INFO

DBHost = os.getenv("DBHOST", "LFXMongo")
TweetDBNam = "TweetBot"
ArchDBNam = "archive"

# HashTag List
HashTagList = open("assets/hashtags.txt").read().split()
# Handle all Logging to documents via piping from CLI
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LogLevel)
# Gets DB objects
TwtHistDB = MongoDB("history", DBHost, TweetDBNam)
ArchiveDB = MongoDB(ArchDBNam, Indexes="raw", Host=DBHost)


# [Twitter Keys] - From ENV Vars
APKey = os.getenv("CXAPKEY")
# API key Secret
APKeySec = os.getenv("CXAPSEC")
# Access Token
ACTok = os.getenv("ACTOKEN")
# Access Token secret
ACTokSec = os.getenv("ACTOKSEC")
# Generates Twitter Authetication object
tweetAuth = tweepy.Client(
    consumer_key=APKey,
    consumer_secret=APKeySec,
    access_token=ACTok,
    access_token_secret=ACTokSec,
)


def generateTweetBody(DBObject: MongoDB):
    """Generates Twittter ready tweet bodies"""

    def getGood(Renders: dict) -> list:
        """Returns Statments Marked as 'Good'"""
        return [render for render, rating in Renders.items() if rating == "Good"]

    while True:
        # Gets random generations from archive database
        Message = DBObject.random()
        Message.pop("_id")
        Message.pop("chunk")
        # Ensures no break, unless statment is successfully pulled.
        if not TwtHistDB.validate(Message):
            # Parses Statments marked as good
            GoodMsg = getGood(Message.pop("render"))
            if GoodMsg:
                # Pick statment from set
                return random.choices(GoodMsg)[0], Message


def buildHashtags(
    BodyLength: int,
    Hashtags: list = HashTagList,
    CharLimit: int = CharacterLimit,
    TagLimit: int = 3,
):
    """Maximizes the number of Hashtags, with the remaining characters in a post."""
    # If not enough chars for a tag. (Min. 2), return nothing.
    if CharLimit - BodyLength <= 1:
        return

    # randomize Input List
    random.shuffle(Hashtags)

    # Maximize the number of hashtags that can be placed into the remaining amount of characters
    Out = ""
    for Tag in Hashtags:
        # Preps hashtag, adds space and '#' symbol
        PrepTag = "#" + Tag + " "
        # Returns value if length exceeds limit
        if BodyLength + len(Out) + len(PrepTag) > CharLimit:
            return Out
        # returns if Number of tags equals limit
        elif len(Out.split()) == TagLimit:
            return Out
        # if adding tag doesnt go over remaining chars, add it to string
        Out += PrepTag
    return Out


def Wait():
    logging.info(f"Starting wait for: {WaitInt} Hours")
    sleep(WaitInt * 3600)


def main():

    # Startup Logo
    startUp()

    while True:

        Wait()

        TwtNum = TwtHistDB.count() + 1

        logging.info(f"Tweet#{TwtNum}: Generating Tweet")
        # returns a random "Good" render from the archive database
        rawPost, Message = generateTweetBody(ArchiveDB)
        # Add punctuation and hashtag to raw post
        Post = rawPost + "\n" + buildHashtags(len(rawPost), TagLimit=4)

        logging.info(f"Tweet#{TwtNum}:\n{Post}")

        if not ReadOnly:
            logging.info(f"Tweet#{TwtNum}: Posting to Twitter")
            tweetAuth.create_tweet(text=Post)

            logging.info(f"Tweet#{TwtNum}: Pushing Post to History DB")
            Message["tweet"] = Post
            TwtHistDB.push(Message)


if __name__ == "__main__":

    main()
