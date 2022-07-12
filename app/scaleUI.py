from lib.General import *
from lib.Scalelib import *

# [VARS]
DBHost = "127.0.0.1"  # "LFXMongo"
QRend = "render"
DBArch = "archive"
DBCorp = "corpus"

Goal = 5000

rndQueue = Queue(QRend, Host=DBHost)
ArchiveDB = Database(DBArch, Index="raw", Host=DBHost)
CorpusDB = Database(DBCorp, Host=DBHost)


messageZ = {
    "_id": "ObjectId('62c7827dbe77382bcf574bac')",
    "raw": "Did you know you sha\re your birthday with at least 9 other million people in the world",
    "chunk": [
        [["Did", "NNP"]],
        [["know", "VB"], ["share", "NN"]],
        ["birthday", "JJ"],
        ["least", "JJS"],
        ["9", "CD"],
        ["million", "CD"],
        [["people", "NNS"], ["world", "NN"]],
    ],
    "render": [
        "Did you know you llama your birthday with at least 9 other million people in the world",
        "Did you know you share your birthday with at least 9 other million llamas in the world",
        "Did you know you share your birthday with at least 9 other million people in the llama",
    ],
}


def main():

    while True:

        # Pulls message from Render Queue
        message = rndQueue.pull()

        # Provides Fax, returns message object with renders ranked in a dictionary
        finOut = rateFax(message)
        # print(finOut)

        # Push goods to ready Queue (wait til later)

        # Push to Archive DB
        # Archival Data of ALL renders, and components.
        ArchiveDB.push(finOut)

        # Push to Corpus DB
        # Data used to train NLN used to rate future renders automatically
        CorpusDB.push(finOut["render"])

        # Display total data processed / Goal #
        print(f"{CorpusDB.count()}/{Goal} total statment-sets saved to CorpusDB\n")

        # Ask to quit?
        askQuit()

        # Quick nap
        sleep(0)


main()
