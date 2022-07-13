from pymongo import MongoClient
import pymongo.errors
from time import sleep, time
import logging
import hashlib


# Mongo DB Lib
class MongoDB:
    """Connects to Specified MongoDB"""

    def __init__(self, Host=None) -> None:
        if Host:
            ConnectString = f"mongodb://{Host}:27017"
        else:
            ConnectString = "mongodb://127.0.0.1:27017"
        self.Conn = MongoClient(ConnectString)


class Database(MongoDB):
    """Interacts with a Database Collection, in MongoDB"""

    def __init__(
        self, CollectionName, DBName=None, Index: str = None, Host=None
    ) -> None:
        super().__init__(Host)
        if DBName is None:
            DBName = "General"
        self.Col = self.Conn[DBName][CollectionName]
        if Index:
            # Sets Index on Raw attribute
            self.Col.create_index(Index)

    def push(self, Insert):
        """Pushes data to MongoDB Collection"""
        logging.debug(f"Pushing data to Database Collection: {Insert}")
        if isinstance(Insert, list):
            self.Col.insert_many(Insert)
        else:
            self.Col.insert_one(Insert)

    def pull(self, Num: int = 1) -> dict:
        """Pulls data from MongoDB Collection"""
        logging.info("Pulling data from Database Collection")
        return self.Col.find(limit=Num)

    def validate(self, Data: dict) -> bool:
        """Input Raw Queue message, returns True if statment was already processed."""
        if self.Col.find_one(Data):
            return True
        return False

    def count(self) -> int:
        """Counts Documents in a MongoDB Collection"""
        return self.Col.count_documents({})


# Im lazy, and speed is not a concern
# Fight me
class Queue(MongoDB):
    """Interacts with a Queue-Like Collection"""

    def __init__(self, QueueName, Host=None) -> None:
        super().__init__(Host)
        # Detect if queue exists, if not create queue (Capped Collection)
        if QueueName not in self.Conn["Queue"].list_collection_names():
            self.Conn["Queue"].create_collection(QueueName, capped=True, size=5242880)
        self.Col = self.Conn["Queue"][QueueName]

    def push(self, Insert):
        """Pushes Message to MongoDB Queue"""
        logging.debug(f"Pushing data to Queue: {Insert}")
        if isinstance(Insert, list):
            self.Col.insert_many(Insert)
        else:
            self.Col.insert_one(Insert)

    def pull(self) -> dict:
        """Pulls Message from MongoDB Queue\n
        Data will be removed from Queue, once pulled."""
        logging.info("Pulling data from Queue")
        return self.Col.find_one_and_delete({})

    def pullSafe(self) -> dict:
        """Pulls Message from MongoDB Queue\n
        Pulls will not be removed from Queue."""
        logging.info("Safely Pulling data from Queue")
        return self.Col.find_one()

    def pop(self, message) -> dict:
        """Removes Message from MongoDB Queue\n
        Requires pulled message to remove."""
        logging.info("Removing data from Queue")
        message.pop("render")
        return self.Col.delete_one(message)

    def threshold(self, MsgMax=100, Threshold=0.7) -> None:
        """returns if queue is not at max"""
        if self.Col.count_documents({}) < MsgMax:
            logging.info("Threshold not met.")
            return
        # Msg Queue is at Max Threshold
        # Waits until Queue is at Threshold %
        logging.info("Begining Sleep")
        while True:
            sleep(10)
            if self.Col.count_documents({}) < MsgMax * Threshold:
                logging.info("Queue fell under the defined Threshold, Ending Sleep.")
                return

    def count(self) -> int:
        """Counts Messages a MongoDB Queue"""
        return self.Col.count_documents({})


class prefTest:
    """Gets Preformance Metrics Test for Llamafax"""

    def __init__(self) -> None:
        self.docCount = 0
        self.startTime = time()

    def includeOne(self):
        """Adds to the doc count"""
        self.docCount += 1

    def stop(self, Include) -> float:
        """Stops Test, returns Documents per Second
        \nOptional: Include == files to include before stop"""
        self.docCount += Include
        return self.docCount / round((time() - self.startTime), ndigits=2)

    def vstop(self, Units="Messages") -> float:
        """Same as .stop(), but is verbose to console. Only works if logging is info or debug
        \nStops Test, returns Documents per Second
        """
        if self.docCount:
            logging.info(
                f"{round((self.docCount / round((time() - self.startTime),ndigits=2)),ndigits=2)} {Units} per Second Processed."
            )
            return
        logging.info("0 Messages Processed.")


def hashPwd(Input: str, Salt: str = "5"):
    return hashlib.sha256((Salt + Input).encode()).hexdigest()


# User-Authetication DB Class
class UAuth(MongoDB):
    """Interacts with an Authentication Collection, in MongoDB"""

    def __init__(self, AuthCol, Host=None) -> None:
        super().__init__(Host)
        self.Col = self.Conn["AuthNZ"][AuthCol]
        # creates Index for "upn" data, if it doesnt exist
        self.Col.create_index("email", unique=True)
        self.Col.create_index("upn", unique=True)

    def addUser(self, Upn, Pwd, Email, Name, Score=0):
        try:
            self.Col.insert_one(
                {
                    "upn": f"{Upn}",
                    "pwd": f"{hashPwd(Pwd)}",
                    "email": f"{Email}",
                    "name": f"{Name}",
                    "score": Score,
                    "locked": True
                }
            )
        except pymongo.errors.DuplicateKeyError:
            return False
        return True

    def valCreds(self, Upn: str, Pwd: str):
        # Get user object that matches email/upn provided
        UserObj = list(self.Col.find({"upn": {"$exists": "true", "$in": [f"{Upn}"]}}))
        if not UserObj:
            UserObj = list(
                self.Col.find({"email": {"$exists": "true", "$in": [f"{Upn}"]}})
            )
        if UserObj and dict(UserObj[0])["pwd"] == hashPwd(Pwd):
            DictT = dict(UserObj[0])
            DictT.pop("pwd")
            return DictT

    def addtoScore(self, UAuthObj: dict, Mod=1):
        UAuthObj.pop("_id")
        if self.Col.update_one(UAuthObj, {"$set": {"score": UAuthObj["score"] + Mod}}):
            return True
        return False

    def count(self) -> int:
        """Counts Documents in a MongoDB Collection"""
        return self.Col.count_documents({})


def makeXDigits(Input: int, Mod: int = 10) -> str:
    """Sets Input strings with leading '0's to make the number a set amount of digits. (Mod)"""
    Digits = len([char for char in str(abs(Input))])
    if Digits >= Mod:
        return str(Input)
    return ("0" * (Mod - Digits)) + str(Input)


def main():

    DBAuth = "userAuth"
    AuthDB = UAuth(DBAuth, Host="10.4.18.2")

    # print(makeXDigits(1567))

    # print(AuthDB.valCreds("james@email.com", "password"))

    print(AuthDB.addUser("jimmer", "YourMom!!1", "james.immer@outlook.com", "James"))

    UsrAuth = {
        "_id": 'ObjectId("62cb7819c205a7060a62f308")',
        "upn": "jimmer",
        "pwd": "f1ae205d286871b66ded534f9bee2e3ddec603fd547912a1b7d906a5d1df05a3",
        "email": "james@email.com",
        "name": "James",
        "score": 53,
    }

    # AuthDB.addtoScore(UsrAuth)

    # AuthDB.push({"upn":"james","pwd":"password"})


if __name__ == "__main__":
    main()
