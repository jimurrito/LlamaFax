from lib.General import *
from lib.Renderlib import *

# [VARS]
DBHost = "LFXMongo" #"127.0.0.1"
QChunk = "chunk"
QRend = "render"
Scope = ["NN", "NNS"]

"""
[Notes]
> Store Llama Corpus data in Renderlib.py
> look into noise vs random
=> if random, regenerate seen on each load/loop
> Sleep when Chunk queue is empty
> sleep when render queue is at threshold
> pull from chunk queue
> take POS (Parts of Speech), and replace with equivelent POS from corpus
=> take chunks, and parse for only in scope POS
=> for each chunk left, replace in the statment in all places that are relevent
=> all statments appended to a list and returned
"""

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    chkQueue = Queue(QChunk, Host=DBHost)
    rndQueue = Queue(QRend, Host=DBHost)
    prefObj = prefTest()

    while True:
        # PrefCatch
        if (chkQueue.count() <= 0) or (rndQueue.count() >= 100):
            prefObj.vstop() 
            prefObj = prefTest()

        # Check if Chunk Queue has active messages
        # if no messages, sleep
        logging.info(f"Messages currently in Chunk Queue: {chkQueue.count()}")
        if not chkQueue.count():
            logging.info("Begining Sleep")
            while True:
                sleep(10)
                if chkQueue.count():
                    logging.info("Ending Sleep")
                    break

        # Checks if Render Queue is at the desired threshold
        logging.info(f"Messages currently in Render Queue: {rndQueue.count()}")
        rndQueue.threshold()

        # Pulls Message from Chunk Queue
        logging.info("Pulling from Chunk Message Queue")
        chunk = chkQueue.pull()

        # Renders Statments, Appends to chunk object
        chunk["render"] = render(chunk, Scope)
        logging.info(f"Rendered Statments:")
        [print(rend) for rend in chunk["render"]]

        # Push new chunk object to render queue for vetting
        logging.info("Pushing to Render Message Queue")
        rndQueue.push(chunk)

        # Add Count to Perf
        prefObj.includeOne()

        # Quick wait
        sleep(0)


main()
