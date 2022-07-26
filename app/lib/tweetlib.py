# libarary for llamafax twitter bot
import os
import tweepy


def startUp():
    print(
        f"""
        ████████╗██╗    ██╗███████╗███████╗████████╗██████╗  ██████╗ ████████╗
        ╚══██╔══╝██║    ██║██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝
           ██║   ██║ █╗ ██║█████╗  █████╗     ██║   ██████╔╝██║   ██║   ██║   
           ██║   ██║███╗██║██╔══╝  ██╔══╝     ██║   ██╔══██╗██║   ██║   ██║   
           ██║   ╚███╔███╔╝███████╗███████╗   ██║   ██████╔╝╚██████╔╝   ██║   
           ╚═╝    ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   

            Component of Llamafax

            Build v{os.getenv("BUILDVER", "0.0")}
        """
    )



# Hashtag management

# > Pulls down Trending hashtags
# > places Trending & Static hashtags into a list
# > Runs all concurrently via Mutli-processing.
# > hashtags proccessing:
#   > checks if hashtag is already present in the collection
#   > evaluates the degree of trending
#       > Optionally compares new trending score against old
#       > averages new and old score, saves as new score.
# > uses score to represent the degree of "Trending" for each of the tags
#       > Determine which, trending and static, tags to use based:
#           - Remaining whitespace
#           - degree of trending
# > returns desired hashtags
#
# <><> IMPORTANT <><>
# Before the full implementation of this feature, analysis needs to be done to avoid using controversial tags.
# Controvercy being defined as:
#   - Hate
#   - Politics
#   - Movements - (BLM, Roe vs Wade, etc), dont want to delegitamize the movements with memes.
#   - Tragities - any situation where humans are/were harmed
#
#


def main():
    startUp()


if __name__ == "__main__":
    main()
