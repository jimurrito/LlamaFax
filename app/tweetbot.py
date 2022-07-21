# Twitter bot for Llamafax service
from lib.MongoDB import MongoDB
import os

DBHost = os.getenv("DBHOST", "LFXMongo")

ArchDBNam = "archive"
ArchiveDB = MongoDB(ArchDBNam, Indexes="raw", Host=DBHost)

# Workflow
# > pick random sets from DB, without pulling the entire DB collection
#   > Pick random array index value
#   > pull down 1 item, using index value
#   > pull back ( ObjectID, renders, User)
# > Validate generation against llamafax database collection
# > Pick hashtags (DB Collection or Static File)
# > Post Tweet to twitter
# > Pin submitting users username in comment of post
# > add raw message and/or hashtags to generation Object
# > Save to Tweet Collection in General DB


# get generations from archive database
ArchiveDB.Col.find()