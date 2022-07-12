from lib.General import *
from time import sleep
import nltk
from nltk.corpus import stopwords
import string
import logging

# [VARS]
DBHost = "LFXMongo" #"127.0.0.1"
QRaw = "raw"
QChunk = "chunk"
ChunkPattern = "NP: {<DT.?>*<JJ.?>*<VB.?>?<NN.?>+}"
NLTKLibs = ["stopwords", "averaged_perceptron_tagger", "vader_lexicon", "punkt"]
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def processRaw(Input, ChunkPat=ChunkPattern):
    """Input == Statment
    \n> Tokenizes
    \n> Removes Stop Words and Punctuation
    \n> Converts to Text() class
    \n> Tags POS Type onto Tokenized test
    \n> Uses an input ChunkPattern (Regex), to chunk the tagged statments"""
    #
    # Tokenizes & removes Punctuation
    logging.debug(f"Working on: {Input}")
    logging.debug("Tokenizing")
    tokens = [
        token for token in nltk.word_tokenize(Input) if token not in string.punctuation
    ]
    # Removes Stop words
    ftokens = [word for word in tokens if word not in stopwords.words("english")]
    text = nltk.Text(ftokens)
    logging.debug("Tagging")
    tag = nltk.pos_tag(text)
    logging.debug("Chunking")

    return nltk.RegexpParser(ChunkPat).parse(tag)


def structure(Raw, Chunk) -> dict:
    return {"raw": Raw, "chunk": Chunk}


def main():
    # Download / Update NLTK libarries
    nltk.download(NLTKLibs)

    # Set Queue Vars
    rawQueue = Queue(QRaw,Host=DBHost)
    chkQueue = Queue(QChunk,Host=DBHost)
    prefObj = prefTest()

    while True:
        # PrefCatch
        if (rawQueue.count() <= 0) or (chkQueue.count() >= 100):
            prefObj.vstop() 
            prefObj = prefTest()

        # Check if Raw Queue has active messages
        # if no messages, sleep
        logging.info(f"Messages currently in Raw Queue: {rawQueue.count()}")
        if not rawQueue.count():
            logging.info("Begining Sleep")
            while True:
                sleep(10)
                if rawQueue.count():
                    logging.info("Ending Sleep")
                    break

        # Checks if Chunk Queue is at the desired threshold
        logging.info(f"Messages currently in Chunk Queue: {chkQueue.count()}")
        chkQueue.threshold()

        logging.info("Begining Run")

        # Pull single message from Raw Queue
        raw = rawQueue.pull()["data"]

        # Process Data into Chunks
        logging.info("Processing Raw Data.")
        chunk = processRaw(raw)

        # Push Message to Chunk Queue
        logging.info("Pushing to Chunk Message Queue")
        chkQueue.push(structure(raw, chunk))

        # Add Count to Perf
        prefObj.includeOne()

        sleep(0)  # https://stackoverflow.com/a/7273727


main()
