# Twitter bot for Llamafax service
import random
import tweepy
from lib.MongoDB import MongoDB
import logging
import os


# [VARS]
LogLevel = logging.INFO
# DBHost = os.getenv("DBHOST", "LFXMongo")
DBHost = "10.4.18.2"
TweetDBNam = "TweetBot"
ArchDBNam = "archive"

CharacterLimit = 280
# hashtags that never change
staticHashTags = ["funny", "animal", "llamas", "memes"]
# latest trending tags
dynamicHashTags = [""]


# Handle all Logging to documents via piping from CLI
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LogLevel)


TwtHistDB = MongoDB("history", DBHost, TweetDBNam)
ArchiveDB = MongoDB(ArchDBNam, Indexes="raw", Host=DBHost)


# [Twitter Keys]
APKey = "RONFnj4FkEAbmKkDLeYrcoLXo"
# API key Secret
APKeySec = "sszPWRvxTP0eslCaG7DrMTTLm0yaMW6H6nJ6beRUJMFA43yYu5"
# Access Token
ACTok = "1545325066602156033-EFRXUkbYRfxZzepJWAh2Plu4CMeTo6"
# Access Token secret
ACTokSec = "ueowEhiWGPlvoxue0y34eU3qQquqVwdPyntkuh4d6Zz6p"
# Generates Twitter Authetication object
tweetAuth = tweepy.Client(
    consumer_key=APKey,
    consumer_secret=APKeySec,
    access_token=ACTok,
    access_token_secret=ACTokSec,
)


# Workflows
#
# [Primary] 0
# 0> pick random sets from DB, without pulling the entire DB collection
#   X> Pick random array index value
#   X> pull down 1 item, using index value
#   X> pull back ( ObjectID, renders, User)
#   0> Built random method for database class objects
# 0> Validate generation against Tweetbot History collection
# 0> Pick hashtags (Hashtag Collection)
# 0> Post Tweet to twitter
# X> Pin submitting users username in comment of post
# 0> add raw message and/or hashtags to generation Object
# 0> Save to DB History Collection
#
# [Secondary]
# Hash-tag processing - [WAIT]
# > Pulls trending tags, and holds them in a database.
#   > trending tags are pulled, and dated. tags need to be re-evaluated to ensure relivance.
#   > Tags should be evaludated for sentiment. want to ensure no hastags of tragities are used.
# > Static hashtags will need to be manually imported.
#   > if trending tag stays relevant for a given threshold, it should be moved to a static state.
# > Weights need to be assigned to the tags to show the priority of use. Random will not cut it.
#   > Weight will be 0-1, and be represented as a float. 0 being the lowest, and 1 being the highest.
# Sentiment Analysis
# > Evalutes the number of likes and retweets to re-enforce the quality of the rendered statment.
# > This data will be used to help train the rating engine


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
    Hashtags: list = staticHashTags,
    CharLimit: int = CharacterLimit,
    TagLimit: int = 3,
):
    """"""
    # Intakes |> Length: Int, where Int is the number of characters in the body
    #         |> Hashtags: List, hashtags to be appended
    # Ouputs |> Tags that maximize the number of hashtags, while also not exceeding the char limit

    # If not enough chars for a tag. (Min. 2), return nothing.
    if CharLimit - BodyLength <= 1:
        return

    # Maximize the number of hashtags that can be placed into the remaining amount of characters
    Out = ""
    ct = 0
    for Tag in Hashtags:
        # Preps hashtag, adds space and '#' symbol
        PrepTag = "#" + Tag + " "
        # Returns value if length exceeds limit
        if BodyLength + len(Out) + len(PrepTag) > CharLimit:
            return Out
        # returns if Number of tags equals limit
        elif ct == TagLimit:
            return Out
        # if adding tag doesnt go over remaining chars, add it to string
        Out += PrepTag
        ct += 1
    return Out


def main():

    # returns a random "Good" render from the archive database
    rawPost, Message = generateTweetBody(ArchiveDB)
    # Add punctuation and hashtag to raw post
    Post = rawPost + "\n" + buildHashtags(len(rawPost))

    # Temp Confirm
    print(Post)
    while True:
        Input = input("(y)es or (n)o? ")

        if Input == "n":
            print("Discarded")
            break

        elif Input == "y":
            tweetAuth.create_tweet(text=Post)
            Message["tweet"] = Post
            # print(Message)
            TwtHistDB.push(Message)
            break
        else:
            print(f"Invalid Input: {Input}")


if __name__ == "__main__":

    main()
