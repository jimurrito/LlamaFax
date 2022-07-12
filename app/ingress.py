from lib.General import *
from lib.Ingresslib import *
import logging

# [VARS]
LogLevel = logging.INFO
DBHost = "LFXMongo" #"127.0.0.1"
QueueName = "raw"
DBArch = "archive"


# Ninja API
NinjaAPI_Enable = True
Categories = CATSch.allCats.value

# Constants
# Handle all Logging to documents via piping from CLI
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LogLevel)

# Sets Queue Object
queue = Queue(QueueName,Host=DBHost)
# Sets Archive DB Object
ArchiveDB = Database(DBArch, Index="raw", Host=DBHost)

# Gets API keys from cli
NinjaAPIKey, ScrapValues = getArgs()
if ScrapValues:
    logging.warning(f"Undefined Values provided {ScrapValues}")


def NinjaAPI(Enable=True):
    if not Enable:
        raise Exception("Ninja API Calls not Enabled")
    logging.info(f"Calling API Ninja Category: Fact")
    IngressSet = getAPINinja(NinjaAPIKey)
    logging.debug(f"Call returned: {len(IngressSet)} Statments")
    badItemCT = 0
    for Ingress in IngressSet:
        # Validate Fact is Unique before push
        if ArchiveDB.validate(Ingress):
            logging.warning("Fact injested was already Proccessed")
            badItemCT += 1
        # Inject into Queue
        queue.push(strip(Ingress))
    return badItemCT


def main():
    prefObj = prefTest()
    while True:
        logging.info(f"Messages currently in Queue: {queue.count()}")
        # Show preformance on wait (temp fix)
        if queue.count() >= 100:
            prefObj.vstop() 
            prefObj = prefTest()
        
        # Wait and Check Threshold
        queue.threshold()
        logging.info("Begining Run")
        # Calls Ninja API, Injects to Message Queue
        badItems = NinjaAPI(NinjaAPI_Enable)

        # Add Count to Perf (Minus facts that are not unique)
        prefObj.docCount += (20 - badItems)

        sleep(0) #https://stackoverflow.com/a/7273727


main()
